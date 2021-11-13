$(document.registration).ready(function() {

    $('input').keyup(function() {
      // set password variable
      var password = $(this).val();
      var p1 = document.getElementById("clave1").value;
      var p2 = document.getElementById("clave2").value;
      var noValido = / /;
    
      //validar longitud contraseña
      if ( password.length < 8 ) {
          $('#length').removeClass('valid').addClass('invalid');
      } else {
          $('#length').removeClass('invalid').addClass('valid');
      }
      //validar letra
      if ( password.match(/[A-z]/) ) {
          $('#letter').removeClass('invalid').addClass('valid');
      } else {
          $('#letter').removeClass('valid').addClass('invalid');
      }
    
      //validar letra mayúscula
      if ( password.match(/[A-Z]/) ) {
          $('#capital').removeClass('invalid').addClass('valid');
      } else {
          $('#capital').removeClass('valid').addClass('invalid');
      }
    
      //validar caracter
      if ( password.match(/[$@$!%*?&.,_#]/) ) {
          $('#caracter').removeClass('invalid').addClass('valid');
      } else {
          $('#caracter').removeClass('valid').addClass('invalid');
      }
    
      //validar numero
      if ( password.match(/\d/) ) {
          $('#number').removeClass('invalid').addClass('valid');
      } else {
          $('#number').removeClass('valid').addClass('invalid');
      }
    
      if(p1 != "" && p2 != ""){
    
        //validar confirmación contraseña
        if (p1.length == 0 || p2.length == 0) {
          $('#null').removeClass('valid').addClass('invalid');
        } else {
          $('#null').removeClass('invalid').addClass('valid');
        }
    
        //validar contraseñas cohincidan
        if (p1 != p2) {
          $('#match').removeClass('valid').addClass('invalid');
        } else {
          $('#match').removeClass('invalid').addClass('valid');
        }
        
        // se chequea el regex de que el string no tenga espacio
        if(noValido.test(p1 || p2)){ 
          $('#blank').removeClass('valid').addClass('invalid');
        } else {
          $('#blank').removeClass('invalid').addClass('valid');
        }
      }
    
    }).focusout(function() {
        $('#pswd_info').hide();
      }).focus(function() {
        $('#pswd_info').show();
    });
    });