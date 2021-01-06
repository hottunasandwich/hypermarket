url1 = 'http://127.0.0.1:5000/api/product/list'
url2 = 'http://127.0.0.1:5000/api/product/delete/'
url3 = 'http://127.0.0.1:5000/api/product/get_category'
url4 = 'http://127.0.0.1:5000/api/product/edit'
url5 = 'http://127.0.0.1:5000/api/product/add'


function makeTable(url){
    $.get(url).done(function(resp){
    $('.mytable').empty()
    var $table = '<table class="table table-striped"><tr><th>تصوير</th>';
    $table += '<th>نام كالا</th><th>دسته‌بندي</th>' + '<th></th></tr>';
    resp.forEach(function(i){
        $table += "<tr><td>"+ '<img class="img-thumbnail" src="'+ i.image_link +'" width="100">'
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
            console.log("Taaaamam")
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
    resp.forEach(function(i){
        var $option = "<option>"+ i + "</option>"
        $("#cat-add, #category-select").append($option)
    })
    $(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop()
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName)
    })
})

$("#final-pro-add").click(function(e){
//    if ($("#pro-add").val() && $("#cat-add").val())
//        $.post(url5,{'name': $("#pro-add").val(), 'category': $("#cat-add").val()},alert)
    if ($("#pro-add").val() && $("#cat-add").val() && $("#img-add").val()){
        var form_data = new FormData()
        e.preventDefault()
        form_data.append('file', $('#add-form').prop('files')[0])
        console.log(form_data)
        $.post(url5,form_data,alert)
        console.log("HI LADY")
        }//{'name': $("#pro-add").val(), 'category': $("#cat-add").val(), 'img': this}
    else
        null
})

$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: url5,
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
            },
        });
    });
});