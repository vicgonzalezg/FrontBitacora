/* Función para cambiar el estado de los usuarios. */
function cambiaNombre(cb){
    if (cb.checked) {
        $('label[for="flexCheckChecked"]').text('Habilitado');
    }
    else {
        $('label[for="flexCheckChecked"]').text('Deshabilitado');
    }
};

/* Función para validar el email */
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

/* Función para validar el telefono */
function validateTelefono(telefono) {
    var phoneno = /^[0-9]+$/;
    return phoneno.test(String(telefono))
}
/* ------------------------------ LOGIN ----------------------------------------*/
//validar email login y recuperar contraseña
function loginUsuarios() {
    event.preventDefault();
    var email = document.getElementById("email").value

    if (!(validateEmail(email))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }
}  
/* ------------------------------ USUARIOS -------------------------------------*/
//Crear usuarios Administradores
function crearAdmin() {
    event.preventDefault();
    var nombre = document.getElementById("nombreAdmin");
    var apellido = document.getElementById("apellidoAdmin");
    var email = document.getElementById("emailAdmin");
    var telefono = document.getElementById("telefonoAdmin");
    var idioma = document.getElementById("idiomaAdmin");
    
    if (nombre.value == "" || apellido.value == "" || email.value == "" || telefono.value == "" || idioma.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    }
    else if (!(validateEmail(email.value))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }
    else if (!(validateTelefono(telefono.value))) {
        Swal.fire('Favor revisar número telefónico!', '', 'warning')
    }else if (telefono.value.length < 8 || telefono.value.length > 10){
        Swal.fire('Número telefónico debe contener entre 8 a 10 digitos.', '', 'warning')
    }
    else {
        var formAdmin = document.forms["formAdmin"];
        Swal.fire({
            title: '¿Está seguro de crear al usuario Administrador?',
            showDenyButton: true,
            icon: 'question',
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                    formAdmin.submit();   
            }
        });
    }
}

//Crear usuarios Coach
function crearCoach() {
    event.preventDefault();
    var nombre = document.getElementById("nombreCoach");
    var apellido = document.getElementById("apellidoCoach");
    var email = document.getElementById("emailCoach");
    var telefono = document.getElementById("telefonoCoach");
    var idioma = document.getElementById("idiomaCoach");

    if (nombre.value == "" || apellido.value == "" || email.value == "" || telefono.value == "" || idioma.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    } else if (!(validateEmail(email.value))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }
    else if (!(validateTelefono(telefono.value))) {
        Swal.fire('Favor revisar número telefónico!', '', 'warning')
    }else if (telefono.value.length < 8 || telefono.value.length > 10){
        Swal.fire('Número telefónico debe contener entre 8 a 10 digitos.', '', 'warning')
    }
    else {
        var form = document.forms["formCoach"];

        Swal.fire({
            title: '¿Está seguro de crear al usuario Coach?',
            showDenyButton: true,
            icon: 'question',
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                    form.submit();
            } 
        });
    }
}

//Crear usuarios Coachee
function crearCoachee() {
    event.preventDefault();
    var nombreEmp = document.getElementById("nombreEmpCoachee");
    var idioma = document.getElementById("idiomaCoachee");
    var nombre = document.getElementById("nombreCoachee");
    var apellido = document.getElementById("apellidoCoachee");
    var nombreJefe = document.getElementById("nombreJefeCoachee");
    var apellidoJefe = document.getElementById("apellidoJefeCoachee");
    var email = document.getElementById("emailCoachee");
    var emailJefe = document.getElementById("emailJefeCoachee");
    var telefono = document.getElementById("telefonoCoachee");
    var telefonoJefe = document.getElementById("telefonoJefeCoachee");

    if (nombreEmp.value == "" || nombre.value == "" || apellido.value == "" || email.value == "" || telefono.value == "" || idioma.value == "" ||
        nombreJefe.value == "" || apellidoJefe.value == "" || emailJefe.value == "" || telefonoJefe.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    } else if (!(validateEmail(email.value)) || !(validateEmail(emailJefe.value))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }
    else if (!(validateTelefono(telefono.value)) || !(validateTelefono(telefonoJefe.value))) {
        Swal.fire('Favor revisar número telefónico!', '', 'warning')
    }else if (telefono.value.length < 8 || telefono.value.length > 10 || telefonoJefe.value.length < 8 || telefonoJefe.value.length > 10){
        Swal.fire('Número telefónico debe contener entre 8 a 10 digitos.', '', 'warning')
    }
    else {
        var form = document.forms["formCoachee"];

        Swal.fire({
            title: '¿Está seguro de crear al usuario Coachee?',
            showDenyButton: true,
            icon: 'question',
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            if (result.isConfirmed) {
                    form.submit();
            } 
        });
    }
}

//Modificar Usuarios
//Administradores
function modificarAdmin(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var nombre = document.getElementById("nombreAdmin"+'-'+id);
    var apellido = document.getElementById("apellidoAdmin"+'-'+id);
    var email = document.getElementById("emailAdmin"+'-'+id);
    var telefono = document.getElementById("telefonoAdmin"+'-'+id);
    var idioma = document.getElementById("idiomaAdmin"+'-'+id);
    if (nombre.value == "" || apellido.value == "" || email.value == "" || telefono.value == "" || idioma.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    }
    else if (!(validateEmail(email.value))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }
    else if (!(validateTelefono(telefono.value))) {
        Swal.fire('Favor revisar número telefónico!', '', 'warning')
    }else if (telefono.value.length < 8 || telefono.value.length > 10){
        Swal.fire('Número telefónico debe contener entre 8 a 10 digitos.', '', 'warning')
    }
    else {
        var formAdmin = document.forms["formAdmin-"+id];
        Swal.fire({
            title: '¿Está seguro de los cambios para el usuario Administrador?',
            showDenyButton: true,
            icon: 'question',
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            if (result.isConfirmed) {
                    formAdmin.submit();
            } 
        });
    }
}

//Coach
function modificarCoach(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var nombre = document.getElementById("nombreCoach"+'-'+id);
    var apellido = document.getElementById("apellidoCoach"+'-'+id);
    var email = document.getElementById("emailCoach"+'-'+id);
    var telefono = document.getElementById("telefonoCoach"+'-'+id);
    var idioma = document.getElementById("idiomaCoach"+'-'+id);

    if (nombre.value == "" || apellido.value == "" || email.value == "" || telefono.value == "" || idioma.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    } else if (!(validateEmail(email.value))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }
    else if (!(validateTelefono(telefono.value))) {
        Swal.fire('Favor revisar número telefónico!', '', 'warning')
    }else if (telefono.value.length < 8 || telefono.value.length > 10){
        Swal.fire('Número telefónico debe contener entre 8 a 10 digitos.', '', 'warning')
    }
    else {
        var formCoach = document.forms["formCoach-"+id];
        Swal.fire({
            title: '¿Está seguro de los cambios para el usuario Coach?',
            showDenyButton: true,
            icon: 'question',
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            if (result.isConfirmed) {
                    formCoach.submit();
            }
        });
    }
}

//Coachee
function modificarCoachee(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var nombreEmp = document.getElementById("nombreEmpCoachee"+'-'+id);
    var idioma = document.getElementById("idiomaCoachee"+'-'+id);
    var nombre = document.getElementById("nombreCoachee"+'-'+id);
    var apellido = document.getElementById("apellidoCoachee"+'-'+id);
    var nombreJefe = document.getElementById("nombreJefeCoachee"+'-'+id);
    var email = document.getElementById("emailCoachee"+'-'+id);
    var emailJefe = document.getElementById("emailJefeCoachee"+'-'+id);
    var telefono = document.getElementById("telefonoCoachee"+'-'+id);
    var telefonoJefe = document.getElementById("telefonoJefeCoachee"+'-'+id);

    if (nombreEmp.value == "" || nombre.value == "" || apellido.value == "" || email.value == "" || telefono.value == "" || idioma.value == "" ||
        nombreJefe.value == "" || emailJefe.value == "" || telefonoJefe.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    } else if (!(validateEmail(email.value)) || !(validateEmail(emailJefe.value))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }
    else if (!(validateTelefono(telefono.value)) || !(validateTelefono(telefonoJefe.value))) {
        Swal.fire('Favor revisar número telefónico!', '', 'warning')
    }else if (telefono.value.length < 8 || telefono.value.length > 10 || telefonoJefe.value.length < 8 || telefonoJefe.value.length > 10){
        Swal.fire('Número telefónico debe contener entre 8 a 10 digitos.', '', 'warning')
    }
    else {
        var formCoachee = document.forms["formCoachee-"+id];
        Swal.fire({
            title: '¿Está seguro de los cambios para el usuario Coachee?',
            showDenyButton: true,
            icon: 'question',
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            if (result.isConfirmed) {
                    formCoachee.submit();
            } 
        });
    }
}
/*  ------------------------    PROCESOS ------------------------------------------------*/
/* Crear proceso */
function newProceso() {
  event.preventDefault();
  var nombreEmp = document.getElementById("nombreEmpre");
  var cantSesion = document.getElementById("cantiSesiones");
  var fechIni = document.getElementById("fechaInicio");
  var coachProc = document.getElementById("coachProces");
  var coacheeProc = document.getElementById("coacheeProces");
  if (nombreEmp.value == "" || cantSesion.value == "" || fechIni.value == "" || coachProc.value == "Seleccione un Coach" || coacheeProc.value == "Seleccione un Coachee") {
      Swal.fire('Todos los campos son Obligatorios!', '', 'info')
  }  else if( cantSesion.value < 1){
    Swal.fire('La cantidad de sesiones debe ser igual o mayor a 1', '', 'info')
  }
  else
  {
      var formProc = document.forms["formProc"];
      Swal.fire({
          title: '¿Está seguro de crear el proceso?',
          showDenyButton: true, 
          icon: 'question',
          confirmButtonText: `Si`,
          denyButtonText: `No`,
      }).then((result) => {
          if (result.isConfirmed) {
                  formProc.submit();
          } 
      });
  }
}

//Modificar Proceso Administrador
function modProceso(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var nombreEmp = document.getElementById("nombreEmpre"+'-'+id);
    var cantSesion = document.getElementById("cantiSesiones"+'-'+id);
    var fechIni = document.getElementById("fechaInicio"+'-'+id);
    var coachProc = document.getElementById("coachProces"+'-'+id);
    var coacheeProc = document.getElementById("coacheeProces"+'-'+id);
    if (nombreEmp.value == "" || cantSesion.value == "" || fechIni.value == "" || coachProc.value == "" || coacheeProc.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    } 
    else
    {
    var formModProceso = document.forms["formModProceso-"+id];
    Swal.fire({
        title: '¿Estas seguro de realizar los cambios?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'No!',
        confirmButtonText: 'Si, Realizar!'
    }).then((result) => {
        if (result.isConfirmed) {
            formModProceso.submit();
        }
    })
}
}

//Modificar Proceso Coach
function modProcesoCoach(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var objetivosProc = document.getElementById("objetivosProc"+'-'+id);
    var indicadoresProc = document.getElementById("indicadoresProc"+'-'+id);
    if (objetivosProc.value == "" || indicadoresProc.value == "") {
        Swal.fire('Todos los campos son Obligatorios!', '', 'info')
    } 
    else
    {
    var formModProceso = document.forms["formModProcesoCoach-"+id];
    Swal.fire({
        title: '¿Estas seguro de realizar los cambios?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'No!',
        confirmButtonText: 'Si, Realizar!'
    }).then((result) => {
        if (result.isConfirmed) {
            formModProceso.submit();
        }
    })
}
}
/* ######################################################################################### */
/*                                        Sesiones                                            */
//Modificar sesiones Coach
function modSesiones(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var fechaSesion = document.getElementById("fechaSesion"+'-'+id).value;
    var apptime = document.getElementById("apptime"+'-'+id).value;
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }
    today = yyyy + '-' + mm + '-' + dd;

    if (!fechaSesion || !apptime) {
        Swal.fire('Los campos fecha y hora de la sesión son obligatorios!', '', 'info')
    }
    else if (fechaSesion < today ){
        Swal.fire('La fecha no puede ser anterior a la actual!', '', 'info')
    }
    else
    {
    var formSesiones = document.forms["formSesiones-"+id];
    Swal.fire({
        title: '¿Estas seguro de realizar los cambios?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'No!',
        confirmButtonText: 'Si, Realizar!'
    }).then((result) => {
        if (result.isConfirmed) {
            formSesiones.submit();
        }
    })
}
}

//agregar Enlace
function agregarEnlace(elem) {
    var re = /^(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})/;
    event.preventDefault();
    var id = $(elem).data("id");
    var enlace = document.getElementById("link"+'-'+id);
    var formEnlace = document.forms["formEnlace-"+id];
    if (enlace.value == "") {
        Swal.fire('Ingrese un enlace para guardar!', '', 'info')
    }
    else if(!re.test(enlace.value)){
        Swal.fire('Ingrese un enlace valido!', '', 'info')
    }
    else{
        formEnlace.submit();
    }
}
//agregar Archivo
function agregarArchivo(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var archivo = document.getElementById("archivo"+'-'+id);
    
    var formArchivo = document.forms["formArchivo-"+id];
    if (archivo.value == "") {
        Swal.fire('Ingrese un archivo para guardar!', '', 'info')
    }else{
            formArchivo.submit();
}
}

//eliminar Enlace
function eliminarEnlace(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    console.log(id)
    var formEnlaceEliminar = document.forms["formEnlaceEliminar-"+id];
    console.log(formEnlaceEliminar)
    if (formEnlaceEliminar == null) {
        Swal.fire('Ha ocurrido un error al eliminar!', '', 'info')
    }else{
        formEnlaceEliminar.submit();
}
}
//eliminar Archivo
function eliminarArchivo(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var formArchivoEliminar = document.forms["formArchivoEliminar-"+id];
    if (formArchivoEliminar == null) {
        Swal.fire('Ha ocurrido un error al eliminar!', '', 'info')
    }else{
        formArchivoEliminar.submit();
}
}

/* ######################################################################################### */
/*                                        Sesiones Coachee                                   */

//Modificar Respuesta de Avances Coachee
function modSesionesCoachee(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var respuestaAvances = document.getElementById("respuestaAvancesSesion"+'-'+id).value
    if(respuestaAvances == ""){
        Swal.fire('Antes de guardar ingrese datos en "Estado de asignaciones"', '', 'info')
    }else{
    var formSesionesCoachee = document.forms["formSesionesCoachee-"+id];
    Swal.fire({
        title: '¿Estas seguro de realizar los cambios?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'No!',
        confirmButtonText: 'Si, Realizar!'
    }).then((result) => {
        if (result.isConfirmed) {
            formSesionesCoachee.submit();
        }
    })
    }
}

//Modificar Plan de Accion Coachee
function modPlanAccion(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    var planAccionProc = document.getElementById("planAccionProc"+'-'+id).value
   
    var formSesionesCoachee = document.forms["formModProcesoCoachee-"+id];
    Swal.fire({
        title: '¿Estas seguro de realizar los cambios?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'No!',
        confirmButtonText: 'Si, Realizar!'
    }).then((result) => {
        if (result.isConfirmed) {
            formSesionesCoachee.submit();
        }
    })
}

/* ######################################################################################### */
/*                               Recuperacion de Contraseña                                  */
//Cambio de Contraseña 
function recuperarClave() {
    event.preventDefault();
    var email = document.getElementById("email").value

    if (!(validateEmail(email))) {
        Swal.fire('Favor revisar correo electrónico!', '', 'warning')
    }else{
        var formRecuperarClave = document.forms["recuperarClave"];
        formRecuperarClave.submit();
    }

}   
//Cambio de Contraseña 
function cambioclave() {
    event.preventDefault();
    var clave1 = document.getElementById("clave1").value
    var clave2 = document.getElementById("clave2").value
    var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&.,_#])([A-Za-z\d$@$!%*?&.,_#]|[^ ]){8,20}$/;

    if (!regex.test(clave1) || !regex.test(clave2)) {
        Swal.fire('La contraseña no cumple con los requisitos minimos.', '', 'info')
    }
    else
    {
    var formCambioClave = document.forms["cambioclave"];
        formCambioClave.submit();
}
}
