url1 = 'http://127.0.0.1:5000/api/product/list'
url2 = 'http://127.0.0.1:5000/api/product/delete/'
url3 = 'http://127.0.0.1:5000/api/product/get_category'
url4 = 'http://127.0.0.1:5000/api/product/edit'
url5 = 'http://127.0.0.1:5000/api/product/add_file'
url6 = 'http://127.0.0.1:5000/api/product/add_one'


function makeTable(url){
    $.get(url).done(function(resp){
    $('.mytable').empty()
    var $table = '<table class="table table-striped"><tr><th>تصوير</th>';
    $table += '<th>نام كالا</th><th>دسته‌بندي</th>' + '<th></th></tr>';
    resp.forEach(function(i){
        $table += "<tr><td>"+ '<img class="img-thumbnail" src="'+ decodeURIComponent(i.image_link) +'" width="100">'
        $table += "</td><td class='align-middle'>"+ i.product_name +"</td><td class='align-middle'>"+ i.category +"</td>"
        $table += '<td class="align-middle"><button class="btn btn-link text-decoration-none modify-me" id="'+ i.id +'M" data-toggle="modal" data-target="#modifyP"><i class="fa fa-pencil-square-o" aria-hidden="true"></i> ويرايش</button> &nbsp;'
        $table += '<button class="btn btn-outline-danger border-0 delete-me" id="'+i.id+'D" data-toggle="modal" data-target="#deleteP"><i class="fa fa-trash" aria-hidden="true"></i></button></td></tr>'
    })
    $table += "</table>"
    var $rowOption = $('.mytable').append($table)
    $rowOption.find(".delete-me").click(deleteAction)
    $rowOption.find(".modify-me").click(sendModified)
    })
}makeTable(url1)

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
    $("#final-pro-mod").click(function(e){
        if ($("#new-name").val() && $("#category-select").val()){
            e.preventDefault()
            $.post(url4, {'name': $("#new-name").val(), 'category': $("#category-select").val(),
                                                    'id': $modifyId.replace('M',''),},alert)
            $("#final-pro-mod").attr("data-dismiss", "modal")
        }
    })
    makeTable(url1)
}

async function alert(){
    $("#alert").slideDown(1500)
    $("#alert").click(() => $("#alert").hide())
    await new Promise(r => setTimeout(r, 6000))
    $("#alert").slideUp(1500)
}

$.get(url3, function(resp){
    for (const i in resp) {
        var $option = "<option>"+ (resp[i] + " | " + i) + "</option>"
        $("#cat-add, #category-select").append($option)
    }
    $(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop()
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName)
    })
})

$(function() {
    $("#final-pro-add").click(function(e) {
        var formData = new FormData($('#add-form')[0])
        console.log($("#add-form"))
        if ($("#pro-add").val() && $("#cat-add").val()) {
            e.preventDefault()
            $("#final-pro-add").attr("data-dismiss", "modal")
            $.ajax({
            type: 'POST',
            url: url6,
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log("alert")
                makeTable(url1)
            }
        })}
        $("#add-form")[0].reset()
        $("#img-add").val('').clone(true)
    })
})

$(function() {
    $('#upload-file-btn').click(function(e) {
        if ($("#fileUpload").val()) {
            $("#upload-file-btn").attr("data-dismiss", "modal")
            e.preventDefault()
        }
        var form_data = new FormData($('#upload-file')[0])
        $.ajax({
            type: 'POST',
            url: url5,
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                $("#upload-file-btn").attr("data-dismiss", "modal")
                console.log("alert")
                makeTable(url1)
            }
        }).fail(function() {
                if ($("#fileUpload").val())
                    console.log("alert")
            })
    })
})