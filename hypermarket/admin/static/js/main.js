//=======> This is general Js file for all admin pages.  <=======//

// This function will show the successful notifications.
async function alertSuccess(){
    $("#alert-success").slideDown(1500)
    $("#alert-success").click(() => $("#alert-success").hide())
    await new Promise(r => setTimeout(r, 6000))
    $("#alert-success").slideUp(1500)
}

// This function will show the error notifications.
async function alertError(){
    $("#alert-error").slideDown(1500)
    $("#alert-error").click(() => $("#alert-error").hide())
    await new Promise(r => setTimeout(r, 6000))
    $("#alert-error").slideUp(1500)
}

// Bootstrap default function for validation!
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