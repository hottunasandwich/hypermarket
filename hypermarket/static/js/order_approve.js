

var order = {}

$("#button").click(Register)
function Register(){
    
    var $date = $("#date").val()
    order.date = $date
    
    var $phone = $("#phone").val()
    order.phone = $phone
    
    var $address = $("#address").val()
    order.address = $address
    
    var $last_name = $("#last_name").val()
    order.last_name = $last_name
    
    var $first_name = $("#first_name").val()
    order.first_name = $first_name

    var url="http://127.0.0.1:5000/cart/approve"
    $.post(url, order)

}



// $.ajax('/cart/approve', {
//     type: 'POST',  
//     data: { myData: order},
//     success: function (data, status, xhr) {
//         console.log("Success")
//     },
//     error: function (jqXhr, textStatus, errorMessage) {
//         console.log("Success")

//     }
// });







// var xhttp = new XMLHttpRequest();
// xhttp.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//        // Typical action to be performed when the document is ready:
//        console.log('response:', xhttp.responseText);
//     }
// };
// xhttp.open("GET", "/xhttp/api-address", true);
// xhttp.send();