url1 = "http://127.0.0.1:5000/api/order/list"
url2 = "http://127.0.0.1:5000/api/order/"
url3 = "http://127.0.0.1:5000/api/order/table/"
url4 = "http://127.0.0.1:5000/product/"

// To create the main orders table.
function makeTable(url){
    $.get(url).done(function(resp){
    $('.mytable').empty()
    var $table = '<table class="table table-striped"><tr><th>نام كاربر</th><th>مجموع مبلغ</th><th>زمان ثبت ‌سفارش</th><th></th></tr>';
    resp.forEach(function(i){
        $table += "<tr><td>" + i.username + "</td>" + "<td>"+ i.total_cost + "</td>"  + "<td>"+ i.order_time + "</td>"
        $table += '<td><button class="btn btn-link text-decoration-none show-order" id="'+i.order_id+'" data-toggle="modal" data-target="#order-modal">'
        $table += '<i class="fa fa-eye" aria-hidden="true"></i> برسي سفارش</button></td></tr>'
    })
    $table += "</table>"
        // Set function for taking a look to order detail.
    var $rowOption = $('.mytable').append($table)
    $rowOption.find(".show-order").click(orderDetail)
    });
};makeTable(url1)

// This function will create a table of ordered product and show the owner of order.
function orderDetail(){
    var $curButton = $(this)
    $.get(url2 + $curButton.attr("id"), function(resp) {
        $('#order-detail').empty()
        var $detail = "<table><tr><td><b>نام مشتري:</b></td><td></td> &nbsp; &nbsp;<td>" + resp[0].username + "</td></tr>"
        $detail += "<tr><td><b>آدرس:</b></td><td></td> &nbsp; &nbsp;<td>" + resp[0].address + "</td></tr>"
        $detail += "<tr><td><b>تلفن:</b></td><td></td> &nbsp; &nbsp;<td>" + resp[0].phone_number + "</td></tr>"
        $detail += "<tr><td><b>زمان تحويل:</b></td><td></td> &nbsp; &nbsp;<td>" + resp[0].delivery_time + "</td></tr>"
        $detail += "<tr><td><b>زمان سفارش:</b></td><td></td> &nbsp; &nbsp;<td>" + resp[0].order_time + "</td></tr></table>"
        $('#order-detail').html($detail)
        $.get(url3 + $curButton.attr("id")).done(function(resp){
        var $table = '<table class="table table-striped"><tr><th>كالا</th><th>قيمت</th><th>انبار</th><th>تعداد</th></tr>';
        resp.forEach(function(i){
            $table += "<tr><td><a href='"+ url4+ i.pro_id +"'>"+ i.product_name + "</a></td>"
            $table += "<td>"+ i.price + "</td>"
            $table += "<td>"+ i.warehouse_name + "</td>"
            $table += "<td>"+ i.count + "</td></tr>"
        })
        $table += "</table>"
        var $rowOption = $('.ord-table').append($table)
        })
        })
        $('.ord-table').empty()
}