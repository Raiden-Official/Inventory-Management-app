# imports
from flask import Flask, request, redirect, render_template, jsonify
from dbModel import db, Products, Locations, prodMovements, app
import datetime 

db.create_all()

# Index page with action buttons and report of quantity at each Location.
@app.route('/', methods=['GET'])
def index():
    quantityAtEveryLocation = []
    for location in Locations.query.all():
        for product in Products.query.all():
            quantityAtEveryLocation.append([location.name, product.name, getQuantityAtLocation(location.id, product.id)])
    return render_template('index.html', quantityAtEveryLocation = quantityAtEveryLocation, inOutReport = inOutReport())

# url to handle ajax request on movements page.
@app.route('/reqForProdAtLoc')
def reqForProdAtLoc():
    quantityAtEveryLocation = []
    for location in Locations.query.all():
        for product in Products.query.all():
            quantityAtEveryLocation.append({"locationID" : location.id, "locationName" : location.name, "productID" : product.id, "productName" : product.name, "qty" : getQuantityAtLocation(location.id, product.id)})
    return jsonify(quantityAtEveryLocation)

# Products page with addProduct option and a list of products.
@app.route('/products', methods=['GET','POST'])
def products():    
    if request.method == 'GET':
        products = Products.query.all()
        print(products)
        return render_template('products.html', products = products)

    if request.method == 'POST':
        try:
            prodName = request.form['prodName']
            newProduct = Products(name = prodName)
            db.session.add(newProduct)
            db.session.commit()
            return redirect('/products')
        except:
            print("error adding prod")
    
# Products page with addLocation option and a list of locations.
@app.route('/locations', methods=['GET','POST'])
def locations():
    if request.method == 'GET':
        locations = Locations.query.all()
        print(locations)
        return render_template('locations.html', locations = locations)

    if request.method == 'POST':
        try:
            locName = request.form['locName']
            newLocation = Locations(name = locName)
            db.session.add(newLocation)
            db.session.commit()
            return redirect('/locations')
        except:
            print("error adding loc")

# Movements page with addMovement and a list of past movements.
@app.route('/movements' , methods=['GET','POST'])
def movements():
    locations = Locations.query.all()
    products = Products.query.all()
    prodMovementList = prodMovements.query.all()
    if request.method == 'POST':
        if request.form['fromLocation'] == 'None' and request.form['toLocation'] == "None":
                    errorName = 'Both location fields can\'t be none, please try again with correct values'
                    print(errorName)
                    return render_template('movements.html', locations = locations, products = products, prodMovementList = prodMovementList, errorName = errorName)
        try:
            fromLocationID = request.form['fromLocation']
            toLocationID = request.form['toLocation']
            productID = request.form['productID']
            qty = request.form['quantity']
            qtyAtLocation = getQuantityAtLocation(fromLocationID, productID)
            if int(qty) <= qtyAtLocation or request.form['fromLocation'] == 'None':
                newMovement = prodMovements(fromLocationID = fromLocationID, toLocationID = toLocationID, productID = productID, qty = qty)
                db.session.add(newMovement)
                db.session.commit()
                return redirect('/')
            else:
                errorName = 'Not enough '+ Products.query.get(productID).name +'s at ' + Locations.query.get(fromLocationID).name +'. Try a number less than or equal to ' + str(qtyAtLocation) +'.'
                print(errorName)
                return render_template('movements.html', locations = locations, products = products, prodMovementList = prodMovementList, errorName = errorName)
                
        except:
            print('Error adding movement')
    return render_template('movements.html', locations = locations, products = products, prodMovementList = prodMovementList)

# Handle update action from any page with 
# tableFlag : indicating table to be updated 
#   0 : Products query
#   1 : Location query
#   2 : Movement query
# id  : being the key of that table
@app.route('/updateData/<tebleFlag>/update/<int:id>', methods=['GET', 'POST'])
def updateData(tebleFlag, id):
    if tebleFlag == "1": 
        current = Locations.query.get(id)
    elif tebleFlag == "0": 
        current = Products.query.get(id)
    else: 
        current = prodMovements.query.get(id)

    if request.method == 'POST':
        try:
            current.name = request.form['updatedName']
        except:
            current.fromLocationID = request.form['fromLocation']
            current.toLocationID = request.form['toLocation']
            current.productID = request.form['productID']
            current.qty = request.form['quantity']

        try:
            db.session.commit()
            return redirect('/')
        except:
            print("Error updating data")

    return render_template('updateData.html', currentEntry = current, tableFlag = tebleFlag, locations = Locations.query.all(), products = Products.query.all())

# Delete stuff using the below url :
# @app.route('/deleteData/<tableFlag>/delete/<int:id>', methods=['GET', 'POST'])
# def deleteData(tableFlag, id):
# To throw an error on the next page: 
    # change the return from errorPage to the page below with id

# @app.route('/error/<errorName>', methods=['GET', 'POST'])
# def throwError(errorName):
#     if errorName == 'notEnoughQty':
#         errorName = 'Not enough quantity at origin location, please change the quantity and try again.'
#     elif errorName == 'bothNone':
#         errorName = 'Only one location field can be none at a time, please correct it and try again.'
#     return render_template('error.html', errorName = errorName)




# function to get quantity of each product at a given location
# params: locID = location ID of the location where product has to be counted
#         prodID = product ID of the product to be counted at the given location
def inOutReport():
    locations = Locations.query.all()
    products = Products.query.all()
    report = []
    
    for location in locations:
        incoming = 0
        outgoing = 0
        incomingProds = db.session.query(prodMovements).filter(prodMovements.toLocationID == location.id)
        outgoingProds = db.session.query(prodMovements).filter(prodMovements.fromLocationID == location.id)
        for row in incomingProds:
            incoming += row.qty
        for row in outgoingProds:
            outgoing += row.qty
        report.append([location.name, incoming, outgoing])
    return report

def getQuantityAtLocation(locID, prodID):
    incomingProds = db.session.query(prodMovements).filter(prodMovements.toLocationID == locID, prodMovements.productID == prodID)
    outgoingProds = db.session.query(prodMovements).filter(prodMovements.fromLocationID == locID, prodMovements.productID == prodID)

    count = 0
    for row in incomingProds:
        count = count + row.qty
    for row in outgoingProds:
        count = count - row.qty 
    return count if count > 0 else 0
if __name__ == "__main__":
    app.run(debug=True)