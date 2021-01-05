url1 = 'http://127.0.0.1:5000/api/product/list'
url2 = 'http://127.0.0.1:5000/api/product/delete/'


function makeTable(url){
    $.get(url).done(function(resp){
    $('.mytable').empty()
    var $table = '<table class="table table-striped"><tr><th>تصوير</th>';
    $table += '<th>نام كالا</th><th>دسته‌بندي</th>' + '<th></th></tr>';
    resp.forEach(function(i){
        $table += "<tr><td>"+ '<img class="img-thumbnail" src="'+ i.image_link +'" width="100">'
        $table += "</td><td class='align-middle'>"+ i.product_name +"</td><td class='align-middle'>"+ i.category_id +"</td>"
        $table += '<td class="align-middle"><button class="btn btn-link text-decoration-none modify-me" id="'+ i.id +'M" data-toggle="modal" data-target="#modifyP"><i class="fa fa-pencil-square-o" aria-hidden="true"></i> ويرايش</button> &nbsp;'
        $table += '<button class="btn btn-outline-danger border-0 delete-me" id="'+i.id+'D" data-toggle="modal" data-target="#deleteP"><i class="fa fa-trash" aria-hidden="true"></i></button></td></tr>'
    })
    $table += "</table>"
    var $rowOption = $('.mytable').append($table)
    $rowOption.find(".delete-me").click(deleteAction)
//    $rowOption.find(".modify-me").click(sendModified)
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
    $("#final-modify").click(function(e){
        e.preventDefault()
        $("#final-modify").attr("data-dismiss", "modal")
        $.post(url4, {'nameModify': $("#nameModify", '').val(), 'rowId': $modifyId.replace('M','')})
        alert()
    });
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