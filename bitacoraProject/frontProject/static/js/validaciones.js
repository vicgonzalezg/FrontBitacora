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
/* ------------------------------ USUARIOS -------------------------------------*/
//Crear usuarios Administradores
function crearAdmin() {
    event.preventDefault();
    var nombre = document.getElementById("nombreAdmin");
    var apellido = document.getElementById("apellidoAdmin");
    var email = document.getElementById("emailAdmin");
    var telefono = document.getElementById("telefonoAdmin");
    var idioma = document.getElementById("idiomaAdmin");
    //console.log(nombre.value)
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
            //showCancelButton: true,
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
            //    Swal.fire({
            //        title: 'Usuario agregado',
            //        icon: 'success',
            //        timer: 3000,
            //        timerProgressBar: true
            //    }).then(function () {
                    formAdmin.submit();
            //    })
            } else if (result.isDenied) {
                Swal.fire({
                    title: 'Usuario no se ha registrado',
                    icon: 'info',
                    timer: 3000,
                    timerProgressBar: true
                })
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
    //console.log(nombre.value)
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
            //showCancelButton: true,
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
            //    Swal.fire({
            //        title: 'Usuario Coach creado con éxito!',
            //        icon: 'success',
            //        timer: 3000,
            //        timerProgressBar: true
            //    }).then(function () {
                    form.submit();
            //    })
            } else if (result.isDenied) {
                Swal.fire({
                    title: 'Usuario no se ha registrado',
                    icon: 'info',
                    timer: 3000,
                    timerProgressBar: true
                })
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
    //console.log(nombre.value)
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
            //showCancelButton: true,
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
            //    Swal.fire({
            //        title: 'Usuario Coachee creado con éxito!',
            //        icon: 'success',
            //        timer: 3000,
            //        timerProgressBar: true
            //    }).then(function () {
                    form.submit();
            //    })
            } else if (result.isDenied) {
                Swal.fire({
                    title: 'Usuario no se ha registrado',
                    icon: 'info',
                    timer: 3000,
                    timerProgressBar: true
                })
            }
        });
    }
}

//Modificar Usuarios
//Administradores
function modificarAdmin(elem) {
    event.preventDefault();
    var id = $(elem).data("id");
    console.log($('#formAdmin'));
    //alert(id);
    var nombre = document.getElementById("nombreAdmin"+'-'+id);
    var apellido = document.getElementById("apellidoAdmin"+'-'+id);
    var email = document.getElementById("emailAdmin"+'-'+id);
    var telefono = document.getElementById("telefonoAdmin"+'-'+id);
    var idioma = document.getElementById("idiomaAdmin"+'-'+id);
    console.log(nombre.value)
    console.log(apellido.value)
    console.log(email.value)
    console.log(telefono.value)
    console.log(idioma.value)
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
        console.log(formAdmin);
        Swal.fire({
            title: '¿Está seguro de los cambios para el usuario Administrador?',
            showDenyButton: true,
            icon: 'question',
            //showCancelButton: true,
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                //Swal.fire({
                //    title: 'Usuario Administrador actualizado con éxito.',
                //    icon: 'success',
                //    timer: 3000,
                //    timerProgressBar: true
                //}).then(function () {
                //    console.log($('#formAdmin'));
                    formAdmin.submit();
                    
                //})
            } else if (result.isDenied) {
                Swal.fire({
                    title: 'No se ha realizado ningun cambio.',
                    icon: 'info',
                    timer: 3000,
                    timerProgressBar: true
                })
                
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
    //console.log(nombre.value)
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
        console.log(formCoach)
        Swal.fire({
            title: '¿Está seguro de los cambios para el usuario Coach?',
            showDenyButton: true,
            icon: 'question',
            //showCancelButton: true,
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                //Swal.fire({
                //    title: 'Usuario Coach actualizado con éxito!',
                //    icon: 'success',
                //    timer: 3000,
                //    timerProgressBar: true
                //}).then(function () {
                //    console.log($('#formCoach'));
                    formCoach.submit();
                //})
            } else if (result.isDenied) {
                Swal.fire({
                    title: 'No se ha realizado ningun cambio.',
                    icon: 'info',
                    timer: 3000,
                    timerProgressBar: true
                })
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
    //var apellidoJefe = document.getElementById("apellidoJefeCoachee"+'-'+id);
    var email = document.getElementById("emailCoachee"+'-'+id);
    var emailJefe = document.getElementById("emailJefeCoachee"+'-'+id);
    var telefono = document.getElementById("telefonoCoachee"+'-'+id);
    var telefonoJefe = document.getElementById("telefonoJefeCoachee"+'-'+id);
    //console.log(nombre.value)
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
        console.log(formCoachee)
        Swal.fire({
            title: '¿Está seguro de los cambios para el usuario Coachee?',
            showDenyButton: true,
            icon: 'question',
            //showCancelButton: true,
            confirmButtonText: `Si`,
            denyButtonText: `No`,
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
            //    Swal.fire({
            //        title: 'Usuario Coachee actualizado con éxito!',
            //        icon: 'success',
            //        timer: 3000,
            //        timerProgressBar: true
            //    }).then(function () {
                    //console.log($('#formCoachee'));
                    formCoachee.submit();
            //    })
            } else if (result.isDenied) {
                Swal.fire({
                    title: 'No se ha realizado ningun cambio.',
                    icon: 'info',
                    timer: 3000,
                    timerProgressBar: true
                })
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
  //console.log(nombre.value)
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
          //showCancelButton: true,
          confirmButtonText: `Si`,
          denyButtonText: `No`,
      }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
              /* Swal.fire({
                  title:'Proceso creado',
                  icon: 'success',
                  timer: 2000,
                  timerProgressBar: true
              }).then(function(){ */
                  formProc.submit();
              /* }) */
          } else if (result.isDenied) {
              Swal.fire({
                  title:'El proceso no se ha creado',
                  icon: 'info',
                  timer: 2000,
                  timerProgressBar: true
              })
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
            /* Swal.fire({
                icon: 'success',
                timer: 2000,
                title: 'Modificado!',
                text: 'El proceso ha sido actualizado.',
                showConfirmButton: false,
            })
            $('#exampleModal').modal('hide');
            $(".modal-backdrop").remove(); */
            formModProceso.submit();
        }else if (result.isDenied) {
            Swal.fire({
                title: 'No se ha realizado ningun cambio.',
                icon: 'info',
                timer: 3000,
                timerProgressBar: true
            })
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
    var planAccionProc = document.getElementById("planAccionProc"+'-'+id);
    if (objetivosProc.value == "" || indicadoresProc.value == "" || planAccionProc.value == "") {
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
            /* Swal.fire({
                icon: 'success',
                timer: 2000,
                title: 'Modificado!',
                text: 'El proceso ha sido actualizado.',
                showConfirmButton: false,
            })
            $('#exampleModal').modal('hide');
            $(".modal-backdrop").remove(); */
            formModProceso.submit();
        }else if (result.isDenied) {
            Swal.fire({
                title: 'No se ha realizado ningun cambio.',
                icon: 'info',
                timer: 3000,
                timerProgressBar: true
            })
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
    var estadoSesion = document.getElementById("estadoSesion"+'-'+id);
    var descSesion = document.getElementById("descSesion"+'-'+id);
    var asigSesion = document.getElementById("asigSesion"+'-'+id);
    var avancesSesion = document.getElementById("avancesSesion"+'-'+id);
    var link = document.getElementById("link"+'-'+id);
    var proceso = document.getElementById("proceso")
    if (!fechaSesion || !apptime) {
        Swal.fire('Los campos fecha y hora de la sesión son obligatorios!', '', 'info')
    }
    else if (apptime < '08:30:00' || apptime > '19:00:00'){
        Swal.fire('El horario de la sesión debe estar en el rango 08:30 a 19:00 hrs.', '', 'info')
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
            /* Swal.fire({
                icon: 'success',
                timer: 2000,
                title: 'Modificado!',
                text: 'El proceso ha sido actualizado.',
                showConfirmButton: false,
            })
            $('#exampleModal').modal('hide');
            $(".modal-backdrop").remove(); */
            formSesiones.submit();
        }else if (result.isDenied) {
            Swal.fire({
                title: 'No se ha realizado ningun cambio.',
                icon: 'info',
                timer: 3000,
                timerProgressBar: true
            })
        }
    })
}
}