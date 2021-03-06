url1 = 'http://127.0.0.1:5000/api/warehouse/list'
url2 = 'http://127.0.0.1:5000/api/warehouse/delete/'
url3 = 'http://127.0.0.1:5000/api/warehouse/add'
url4 = 'http://127.0.0.1:5000/api/warehouse/edit'

// To create the main warehouse table.
function makeTable(url){
    $.get(url).done(function(resp){
    $('.mytable').empty()
    var $table = '<table class="table table-striped"><tr><th>نام انبار</th><th></th></tr>';
    resp.forEach(function(i){
        $table += "<tr><td>"+ i.warehouse_name + "<td>"+ '<button class="btn btn-link text-decoration-none modify-me" id="'+i.warehouse_id+'M" data-toggle="modal" data-target="#modifyWH"><i class="fa fa-pencil-square-o" aria-hidden="true"></i> ويرايش</button> &nbsp; ';
        $table += '<button class="btn btn-outline-danger border-0 delete-me" id="'+i.warehouse_id+'D" data-toggle="modal" data-target="#deleteWH"><i class="fa fa-trash" aria-hidden="true"></i></button></td></tr>';
    })
    $table += "</table>"
    var $rowOption = $('.mytable').append($table)
    // Set function for delete and modify buttons.
    $rowOption.find(".delete-me").click(deleteAction)
    $rowOption.find(".modify-me").click(sendModified)
    })
}
makeTable(url1)

// Function to send delete data to back server.
function deleteAction() {
    var $delButton = $(this)
    var funcUrl= url2 + $delButton.attr("id")
    $("#final-del").click(function(e){
        e.preventDefault()
        $.get(funcUrl.replace('D',''), () => $delButton.closest('tr').remove())
        .done(alertSuccess)
    })
}


// A function to send a new warehouse name to the back server.
$("#final-add").click(sendNew)
function sendNew(e){
    if ($("#nameWH").val()) {
        e.preventDefault()
        $.post(url3, {'nameWH': $("#nameWH").val()})
        .done(alertSuccess)
        .fail(function(jqXHR, textStatus, errorThrown){
            alertError()
        })
        $("#add-WH-form")[0].reset()
        $("#final-add").attr("data-dismiss", "modal")
        makeTable(url1)
    }
}

// Send modified data to back server.
function sendModified(){
    var $modButton = $(this)
    var $modifyId = $modButton.attr("id")
    $("#final-modify").click(function(e){
        if ($("#nameModify").val()) {
            e.preventDefault()
            $.post(url4, {'nameModify': $("#nameModify").val(), 'rowId': $modifyId.replace('M','')})
            .done(alertSuccess)
            .fail(function(jqXHR, textStatus, errorThrown){
                alertError()
            })
            makeTable(url1)
            $("#mod-form")[0].reset()
            $("#final-modify").attr("data-dismiss", "modal")
        }
    })
}