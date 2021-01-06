url1 = 'http://127.0.0.1:5000/api/inventory_price/list'
url2 = 'http://127.0.0.1:5000/api/inventory_price/delete/'
url3 = 'http://127.0.0.1:5000/api/inventory_price/edit'
url4 = 'http://127.0.0.1:5000/api/inventory_price/detail'
url5 = 'http://127.0.0.1:5000/api/inventory_price/add'

function makeTable(url){
    $.get(url).done(function(resp){
    $('.mytable').empty()
    var $table = '<table class="table table-striped"><tr><th>انبار</th>';
    $table += '<th>كالا</th><th>قيمت</th>' + '<th>موجودي</th><th></th></tr>';
    resp.forEach(function(i){
        $table += "<tr><td>"+ i.warehouse_name +"</td><td>"+ i.product_name +"</td><td>"+ i.price +"</td>"
        $table += "<td>"+ i.number +"</td>"
        $table += '<td><button class="btn btn-link text-decoration-none modify-me" id="'+i.product_id+"-"+ i.ware_id+'" data-toggle="modal" data-target="#modifyIP"><i class="fa fa-pencil-square-o" aria-hidden="true"></i> ويرايش</button> &nbsp;'
        $table += '<button class="btn btn-outline-danger border-0 delete-me" id="'+i.product_id+'D" data-toggle="modal" data-target="#deleteIP"><i class="fa fa-trash" aria-hidden="true"></i></button></td></tr>'
    })
    $table += "</table>"
    var $rowOption = $('.mytable').append($table)
    $rowOption.find(".delete-me").click(deleteAction)
    $rowOption.find(".modify-me").click(sendModified)
    })
}
makeTable(url1)

function deleteAction() {
    var $delButton = $(this)
    var funcUrl= url2 + $delButton.attr("id")
    console.log(funcUrl)
    $("#final-del").click(function(){
        $.get(funcUrl.replace('D',''), () => $delButton.closest('tr').remove())
        alert()
    })
}

function sendModified(){
    var $modButton = $(this)
    var $modifyId = $modButton.attr("id")
    var $allId = $modifyId.split("-")
    $("#final-modify").click(function(e){
        if ($("#new-price").val() && $("#new-inventory").val()){
            e.preventDefault()
            $("#final-modify").attr("data-dismiss", "modal")
            $.post(url3, {'product_id': $allId[0], 'ware_id': $allId[1],'new_price': $("#new-price").val(), 'new-inventory': $("#new-inventory").val()})
            alert()
            makeTable(url1)
        }
        else {
            e.preventDefault()
        }
    })
}
async function alert(){
    $("#alert").slideDown(1500)
    $("#alert").click(() => $("#alert").hide())
    await new Promise(r => setTimeout(r, 6000))
    $("#alert").slideUp(1500)
}

(function() {
  window.addEventListener('load', function() {
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false);
    });
  }, false)
})();

$.get(url4, function(resp){
    resp[0].forEach(function(i){
        var $option1 = "<option>"+ i.id + "/ " +i.product_name+"</option>"
        $("#pro-select").append($option1)
    })
    resp[1].forEach(function(j){
        var $option2 = "<option>"+ j.warehouse_id + "/ " +j.warehouse_name+"</option>"
        $("#ware-select").append($option2)
    })
})

$("#final-inv-add").click(addInventory)
function addInventory(e){
    if ($("#pro-select").val() && $("#ware-select").val() && $("#inv-price").val() && $("#inv-number").val()){
        e.preventDefault()
        var $pro_add = $("#pro-select").val()[0]
        var $ware_add = $("#ware-select").val()[0]
        var $price_add = $("#inv-price").val()
        var $num_add = $("#inv-number").val()
        $.post(url5, {'pro_id': $pro_add.split("/")[0], 'ware_id': $ware_add.split("/")[0],
        'price': $price_add, 'number': $num_add}, alert)
        $("#final-inv-add").attr("data-dismiss", "modal")
        makeTable(url)
    }
    else
        null
}
