
// DELETE //
// $("td").find("a[href]").click(deleteAction)
$("tr").find("td:last").click(deleteAction)
function deleteAction() {
    $(this).closest('tr').remove()
}

$("#register_cart").click(register)

function register(){

    


}