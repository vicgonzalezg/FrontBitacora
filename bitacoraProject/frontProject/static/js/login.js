(function () {
    'use strict'
  
    // Obtener todos los formularios a los que queremos aplicar estilos de validación personalizados de Bootstrap
    var forms = document.querySelectorAll('.needs-validation')
  
    // Hace un bucle sobre ellos y evita la sumisión
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()