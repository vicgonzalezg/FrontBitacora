
    function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

    function validateTelefono(telefono){
    var phoneno = /^[0-9]+$/;
    return phoneno.test(String(telefono))
    }

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
            }
        else
        {
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
                    Swal.fire({
                        title:'Usuario agregado',
                        icon: 'success',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(function(){
                        formAdmin.submit();
                    })
                } else if (result.isDenied) {
                    Swal.fire({
                        title:'Usuario no se ha registrado',
                        icon: 'info',
                        timer: 3000,
                        timerProgressBar: true
                    })
                }
            });
        }
    }

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
                    Swal.fire({
                        title:'Usuario Coach creado con éxito!',
                        icon: 'success',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(function(){
                        form.submit();
                    })
                } else if (result.isDenied) {
                    Swal.fire({
                        title:'Usuario no se ha registrado',
                        icon: 'info',
                        timer: 3000,
                        timerProgressBar: true
                    })
                }
            });
        }
    }

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
        } else if ( !(validateEmail(email.value)) || !(validateEmail(emailJefe.value))) {
            Swal.fire('Favor revisar correo electrónico!', '', 'warning')
            }
        else if ( !(validateTelefono(telefono.value)) || !(validateTelefono(telefonoJefe.value))) {
            Swal.fire('Favor revisar número telefónico!', '', 'warning')
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
                    Swal.fire({
                        title:'Usuario Coachee creado con éxito!',
                        icon: 'success',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(function(){
                        form.submit();
                    })
                } else if (result.isDenied) {
                    Swal.fire({
                        title:'Usuario no se ha registrado',
                        icon: 'info',
                        timer: 3000,
                        timerProgressBar: true
                    })
                }
            });
        }
    }
