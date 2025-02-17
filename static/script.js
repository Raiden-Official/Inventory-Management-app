// Using callback from http request
// url = "http://localhost:5000/reqForProdAtLoc"
function getProdListAtLocation(url, callback){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send()
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                // readyState 4 says that data has been received and status 200 says that the request was successfull
                var resp = xhr.responseText;
                var respJson = JSON.parse(resp);
                callback(respJson);
            }
            else {
                console.log("status not 200, req failed.")
            }
        }
        else {
            console.log("Req still in process.")
        }
    }
}

$("#fromLocation").change(function(){
    var fromLocation = document.getElementById('fromLocation').value
    var productID = document.getElementById('productID').value
    url = "http://localhost:5000/reqForProdAtLoc/"+fromLocation+"/"+productID+""
    console.log(url)
    getProdListAtLocation(url, function(data){
        document.getElementById('errorName').innerHTML = data[0].locationName + " has " + data[0].qty +" "+ data[0].productName + "s."
    })
})



// Using success from .getJSON

// $("#fromLocation").change(function(){
//     $.getJSON("http://localhost:5000/reqForProdAtLoc", function(data){
//         document.getElementById('errorName').innerHTML = data[0].locationName + " has " + data[0].qty +" "+ data[0].productName + "s."
//     })
// })


$("#productID").change(function(){
    $("#fromLocation").change();
})