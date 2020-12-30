url1 = "http://127.0.0.1:5000/api/order/list"
url2 = "http://127.0.0.1:5000/api/order/"

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
    var $rowOption = $('.mytable').append($table)
    $rowOption.find(".show-order").click(orderDetail)
    });
};makeTable(url1)

function orderDetail(){
    var $curButton = $(this)
    $.get(url2 + $curButton.attr("id"), function(resp) {
        $('#order-detail').empty()
        var $detail = "<p class='mb-0'><b>نام مشتري:</b> &nbsp; &nbsp;" + resp[0].username + "</p>"
        $detail += "<p class='mb-0'><b>آدرس:</b> &nbsp; &nbsp;" + resp[0].address + "</p>"
        $detail += "<p class='mb-0'><b>تلفن:</b> &nbsp; &nbsp;" + resp[0].phone_number + "</p>"
        $detail += "<p class='mb-0'><b>زمان تحويل:</b> &nbsp; &nbsp;" + resp[0].delivery_time + "</p>"
        $detail += "<p class='mb-0'><b>زمان سفارش:</b> &nbsp; &nbsp;" + resp[0].order_time + "</p>"
        $('#order-detail').html($detail)
    })
}

