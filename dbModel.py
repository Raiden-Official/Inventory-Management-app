# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

# config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Database table models
class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)

    def __repr__(self):
        return '<id :%r, productName:%r>' % (self.id, self.name)

class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<id :%r, locationName:%r>' % (self.id, self.name)

class prodMovements(db.Model):
    movementID = db.Column(db.Integer, primary_key=True)
    timeStamp = db.Column(db.Date, default = datetime.datetime.now().date())
    qty = db.Column(db.Integer)

    fromLocationID = db.Column(db.Integer, db.ForeignKey('locations.id'))
    fromLocation = db.relationship('Locations', primaryjoin = fromLocationID == Locations.id)

    toLocationID = db.Column(db.Integer, db.ForeignKey('locations.id'))
    toLocation = db.relationship('Locations', primaryjoin = toLocationID == Locations.id)

    productID = db.Column(db.Integer, db.ForeignKey('products.id'))
    productName = db.relationship('Products', primaryjoin = productID == Products.id)

    def __repr__(self):
        return '<id :%r, productName:%r, fromLocation:%r, toLocation:%r, qty:%r>' % (self.movementID, self.productName, self.fromLocation, self.toLocation, self.qty)

