async function alertSuccess(){
    $("#alert-success").slideDown(1500)
    $("#alert-success").click(() => $("#alert-success").hide())
    await new Promise(r => setTimeout(r, 6000))
    $("#alert-success").slideUp(1500)
}

async function alertError(){
    $("#alert-error").slideDown(1500)
    $("#alert-error").click(() => $("#alert-error").hide())
    await new Promise(r => setTimeout(r, 6000))
    $("#alert-error").slideUp(1500)
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