#se importan librerias
from frontProject.models import Usuario
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.core import serializers
from django.template.loader import get_template
from bitacoraProject import settings
from bitacoraProject.wsgi import *
from django.contrib import messages
from weasyprint import HTML, CSS
from datetime import datetime
import requests
from . import services
import json
import base64

# --------------------------------------------definimos el login--------------------------------------------
def login(request):
    if request.method == 'POST':
        #obtenemos credenciales desde formulario html
        username = request.POST.get('user')
        password = request.POST.get('pass')
        # r=services.LoginServices().generate_request(username,password)
        r = requests.post('http://127.0.0.1:8001/login',
                          data={'USUARIO': username, 'CONTRASENA': password})
        #consultamos por respuesta servidor
        if r.status_code == 200:
            #obtenemos los datos desde la api
            result = json.loads(r.content)
            #nombre que se muestra al ingresar
            nombre_usuario = result['USUARIO']['NOMBRE']
            perfil_usuario = result['USUARIO']['PERFIL_ID']
            #datos del perfil del usuario
            nombre = result['USUARIO']['NOMBRE']
            apellido = result['USUARIO']['APELLIDO']
            correo = result['USUARIO']['CORREO']
            fono_usuario = result['USUARIO']['FONO']
            id_usuario = result['USUARIO']['ID']
            #asignamos los datos a la variable que usaremos en las funciones
            datos_usuario = {'nombre': nombre_usuario,
                             'perfil': perfil_usuario,
                             'id': id_usuario,
                             'fono': fono_usuario,
                             'nombreUsuario': nombre,
                             'apellidoUsuario': apellido,
                             'correo': correo}
            #se obtiene token de seguridad que entrega la api
            token = result['TOKEN']
            #se obtiene json con token de seguridad para entregarlo a las vistas
            headers = {
                'content-type': "application/json",
                'authorization': "Bearer " + token
            }
            #se almacen los datos en las cookie para enviar los datos a las vistas
            request.session['Headers'] = headers
            request.session['Perfil_Usuario'] = datos_usuario

            #se consulta por el perfil de usuario
            plantilla = ''
            if perfil_usuario == 1:
                plantilla = 'menuAdmin'
            elif perfil_usuario == 2:
                plantilla = 'menuCoach'
            elif perfil_usuario == 3:
                plantilla = 'menuCoachee'
            #redirige al usuario al perfil correspondiente
            return redirect(plantilla)
        #envia mensaje en caso de credenciales no validas y redirige al login
        else:
            messages.error(request, r.text.replace('"', ''))
            return render(request, 'login/login.html')
    #renderiza la vista de login
    return render(request, 'login/login.html')

#--------------------------------------------Recuperar Contraseña--------------------------------------------
def recuperarClave(request):
    if request.method == 'POST':
        url = 'http://127.0.0.1:8001/recuperaciones-contrasenas'
        email = request.POST.get('email')
        print(email)
        urlCambioPass = 'http://127.0.0.1:8000/cambioclave'
        jsonRecuperaContra ={
            "CORREO":email,
            "URL":urlCambioPass
        }
        print(jsonRecuperaContra)
        response = requests.post(url, json=jsonRecuperaContra)
        print(response.status_code)
        if response.status_code == 200:
            messages.success(request, 'Se enviara un correo con las instrucciones.')
        else:
            messages.success(request, response.text.replace('"', ''))

    return  render(request, 'login/recuperarClave.html')

#-------------------------------------------- Cambio de Contraseña--------------------------------------------
def cambioclave(request, pk):

    if request.method == 'POST':
        pk=pk
        url = 'http://127.0.0.1:8001/recuperaciones-contrasenas/'+ pk +'/'
        clave = request.POST.get('clave1')
        jsonCambiaContra ={
            "CONTRASENA":clave
        }
        response = requests.put(url, json=jsonCambiaContra)
        #print(response.status_code)
        if response.status_code == 200:
            messages.success(request, 'Contraseña cambiada con éxito. Seras redirigido al Login.')
            #return redirect('/')
        else:
            messages.error(request, response.text.replace('"', ''))

    return render(request, 'login/cambioclave.html')



# --------------------------------------------Cierre de sesión--------------------------------------------
def logout(request):
    try:
        #limpia los datos del json que contiene los datos del token
        headers = {'': ''}
        request.session['Headers'] = headers
        return redirect('/')
    #envia error de logout y redirige al login
    except Exception as e:
        messages.warning(request, 'Ha ocurrido un error inesperado')
        return redirect('/')

def get_cashflows(request):

    response_data = {}
    cashflow_set = Usuario.objects.all()
    i = 0
    for e in cashflow_set.iterator():
        c = Usuario(value=e.value, date=str(e.date))
        response_data[i] = c

    return HttpResponse(
        serializers.serialize("json", response_data),
        content_type="application/json"
    )

# --------------------------------------------Perfil de usuarios--------------------------------------------
def perfil(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        url = 'http://127.0.0.1:8001/usuarios'
        usuario = requests.get(url).json()

        data = {
            'usuario': perfil,
            'entity': usuario,
        }
        return render(request, 'Perfil/perfil.html', data)
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# --------------------------------------------Paginas de Menu por Peril--------------------------------------------
#-------------------------------------------- menu admin --------------------------------------------
def menuAdmin(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el prefin de usuario corresponde al de administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&limit=5'
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            urlProcesosCal = 'http://127.0.0.1:8001/procesos?ESTADOPROCESO_ID!=4'
            urlSesionesCalendario = 'http://127.0.0.1:8001/sesiones'
            #obtiene los datos desde la api enviando token de seguridad
            proceso = requests.get(urlProcesos, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstado, headers=headers).json()
            sesionesCalendario = requests.get(urlSesionesCalendario, headers=headers).json()
            procesosCal = requests.get(urlProcesosCal, headers=headers).json()
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            sesionesCalendario3=[]
            #consulta de procesos por estado y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa = p['NOMBREEMPRESA']
                        nombreCoachee = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        correoCoachee = u['CORREO']
                        telefonoCoachee = u['FONO']
                        cantsesiones = p['CANTSESIONES']
                        fechaIni = p["FECHACREACION"]
                        objetivo = p['OBJETIVOS']
                        indicadores = p['INDICADORES']
                        planAccion = p['PLANACCION']
                        nombreJefe = u['NOMBREJEFE']
                        emailJefe = u['EMAILJEFE']
                        fonoJefe = u['FONOJEFE']
                        idProceso = p['ID']
                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE": nombreCoachee,
                            "APELLIDO": apellidoCoachee,
                            "CORREO": correoCoachee,
                            "FONO": telefonoCoachee,
                            "CANTSESIONES": cantsesiones,
                            "OBJETIVOS": objetivo,
                            "FECHACREACION": fechaIni,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,
                            "DESCRIPCION": estadoDescripcion,
                            "ID": idProceso
                        }]
                        #se almacena una array de objetos
                        listados = json + listados
            
            #consulta de sesiones por proceso y usuarios
            for sCal in sesionesCalendario:
                #Descarta las sesiones Finalizadas y sin fecha 
                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                    for pCal in procesosCal:
                        #Descarta los procesos finalizados.
                        if pCal['ESTADOPROCESO_ID'] != 6:
                            for u in usuario:
                                #consulta por el usuario
                                if pCal['COACHEE_ID'] == u['ID']:
                                    #consulta por la id del proceso para traer las sesiones correspondientes
                                    if pCal['ID'] == sCal['PROCESO_ID']:
                                        fechaSesion = sCal['FECHASESION']
                                        estadoSesion = sCal['ESTADOSESION_ID']
                                        nombreEmpresa = pCal['NOMBREEMPRESA']
                                        nombreCoachee = u['NOMBRE']
                                        apellidoCoachee = u['APELLIDO']
                                        #se almacenan los datos en una variable
                                        sesionesCalendario2 = [{
                                            "NOMBREEMPRESA": nombreEmpresa,
                                            "NOMBRE": nombreCoachee,
                                            "APELLIDO": apellidoCoachee,
                                            "FECHASESION": fechaSesion,
                                            "ESTADOSESION_ID":estadoSesion
                                        }]
                                        #se almacena una array de objetos
                                        sesionesCalendario3 = sesionesCalendario2 + sesionesCalendario3   
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listados,
                'sesiones': sesionesCalendario3
            }
            #renderiza la vista y envia los datos
            return render(request, 'menu/menuAdmin.html', data)
        #consulta por el perfil y redirecciona a su plantilla correspondiente
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)
    #si ingresa a la url de menuAdmin sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

#-------------------------------------------- menu coach --------------------------------------------
def menuCoach(request):
    #try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al de coach
        if perfil['perfil'] == 2:
            #se almacena id del usuario para usarlo de filtro para los procesos
            id = perfil['id']
            #se obtiene el dia actual para usarlo como filtro para la fecha de sesiones
            day = datetime.today().strftime('%Y-%m-%d')
            #variable que almacena la url de la api
            urlSesionesDia = 'http://127.0.0.1:8001/sesiones?ordering=-ID&limit=5&FECHASESION=' + \
                str(day)
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-sesiones'
            urlProcesosCal = 'http://127.0.0.1:8001/procesos?ordering=-ID&COACH_ID=' + str(id)
            urlSesionesCalendario = 'http://127.0.0.1:8001/sesiones'
            urlEstadoProceso = 'http://127.0.0.1:8001/estados-procesos'
            #obtiene los datos desde la api enviando token de seguridad
            sesionesDia = requests.get(urlSesionesDia, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstado, headers=headers).json()
            procesosCal = requests.get(urlProcesosCal, headers=headers).json()
            estadoProc = requests.get(urlEstadoProceso, headers=headers).json()
            sesionesCalendario = requests.get(urlSesionesCalendario, headers=headers).json()
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            listadoBar = []
            listadoBarOrdenado = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            sesionesCalendario3=[]
            #consulta de sesiones por proceso, estado y usuarios
            for s in sesionesDia:
                for p in procesosCal:
                    if p['ID'] == s['PROCESO_ID']:
                        for ep in estadoProc:
                            if ep['ID'] == p['ESTADOPROCESO_ID']:
                                estadoProceso = ep['DESCRIPCION']
                                estadoProce = p['ESTADOPROCESO_ID']
                        for e in estado:
                            if s['ESTADOSESION_ID'] == e['ID']:
                                estadoDescripcion = e['DESCRIPCION']
                        for u in usuario:
                            if p['COACHEE_ID'] == u['ID']:
                                nombreEmpresa = p['NOMBREEMPRESA']
                                nombreCoachee = u['NOMBRE']
                                apellidoCoachee = u['APELLIDO']
                                idProceso = p['ID']
                        for uc in usuario:
                            if p['COACH_ID'] == uc['ID']:
                                nombreCoach = uc['NOMBRE']
                                apellidoCoach = uc['APELLIDO']
                                #se almacenan los datos en una variable
                                json = [{
                                    "NOMBREEMPRESA": nombreEmpresa,
                                    "NOMBRE": nombreCoachee,
                                    "APELLIDO": apellidoCoachee,
                                    "DESCRIPCION": estadoDescripcion,
                                    "NOMBRECOACH": nombreCoach,
                                    "APELLIDOCOACH": apellidoCoach,
                                    "ID": idProceso,
                                    "ESTADOPROC": estadoProce,
                                    "DESCRIPCIONPROCE": estadoProceso
                                }]
                                #se almacena una array de objetos
                                listados = json + listados
            
            #consulta de sesiones por proceso y usuarios
            for sCal in sesionesCalendario:
                #Descarta las sesiones Finalizadas y sin fecha 
                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                    for pCal in procesosCal:
                        #Descarta los procesos Finalizados
                        if pCal['ESTADOPROCESO_ID'] != 6:
                            for u in usuario:
                                #consulta por el usuario
                                if pCal['COACHEE_ID'] == u['ID']:
                                    #consulta por la id del proceso para traer las sesiones correspondientes
                                    if pCal['ID'] == sCal['PROCESO_ID']:
                                        fechaSesion = sCal['FECHASESION']
                                        estadoSesion = sCal['ESTADOSESION_ID']
                                        nombreEmpresa = pCal['NOMBREEMPRESA']
                                        nombreCoachee = u['NOMBRE']
                                        apellidoCoachee = u['APELLIDO']
                                        #se almacenan los datos en una variable
                                        sesionesCalendario2 = [{
                                            "NOMBREEMPRESA": nombreEmpresa,
                                            "NOMBRE": nombreCoachee,
                                            "APELLIDO": apellidoCoachee,
                                            "FECHASESION": fechaSesion,
                                            "ESTADOSESION_ID":estadoSesion
                                        }]
                                        #se almacena una array de objetos
                                        sesionesCalendario3 = sesionesCalendario2 + sesionesCalendario3
            
            #consulta de sesiones por proceso
            for sBar in sesionesCalendario:
                for pBar in procesosCal:
                    if pBar['ID'] == sBar['PROCESO_ID']:
                        estadoSesion = sBar['ESTADOSESION_ID']
                        idSesion = sBar['ID']
                        idProceso = pBar['ID']
                        #se almacenan los datos en una variable
                        sesionBarList = [{
                            "IDP":idProceso,
                            "ID":idSesion,
                            "ESTADOSESION_ID":estadoSesion
                        }]
                        #se almacena una array de objetos
                        listadoBar = sesionBarList + listadoBar
                        #se ordena array por id de sesion de menor a mayor
                        listadoBarOrdenado = sorted(listadoBar, key=lambda k: k['ID'])
            #se obtiene la primera pagina del paginador
            page = request.GET.get('page', 1)

            try:
                #se le dan los atributos al paginador, listado de 4 por pagina
                paginator = Paginator(listados, 2)
                #se almacenan los resultados por por pagina
                listado = paginator.page(page)
            #si ocurre un error mostrara pagina no encontrada.
            except:
                raise Http404
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listado,
                'paginator': paginator,
                'sesiones': sesionesCalendario3,
                'sesionBar': listadoBarOrdenado
            }
            #renderiza la vista y envia los datos
            return render(request, 'menu/menuCoach.html', data)
        #si la consulta por perfil no corresponde redirige al usuario a su perfil en el menu principal
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)
    #si ingresa a la url de menuCoach sin token de seguridad redirecciona al login
 #   except Exception as e:
  #      messages.warning(request, 'Ingrese sus credenciales para acceder')
   #     return redirect('/')

#--------------------------------------------menu coachee--------------------------------------------
def menuCoachee(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al de coachee
        if perfil['perfil'] == 3:
            #se almacena id del usuario para usarlo de filtro para los procesos
            id = perfil['id']
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&COACHEE_ID=' + \
                str(id)
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            urlsesion = 'http://127.0.0.1:8001/sesiones'
            #obtiene los datos desde la api enviando token de seguridad
            proceso = requests.get(urlProcesos, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstado, headers=headers).json()
            sesiones = requests.get(urlsesion, headers=headers).json()
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            sesionesCalendario3=[]
            #variable que almacenara los datos de sesiones que se utilizaran para lista de sesiones
            listadoBar = []
            #fijamos cantidad de sesiones como 0
            canSesiones = 0
            #consulta de procesos por usuarios
            for p in proceso:
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa = p['NOMBREEMPRESA']
                        nombreCoachee = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        idProceso = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach = uc['NOMBRE']
                        apellidoCoach = uc['APELLIDO']
                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE": nombreCoachee,
                            "APELLIDO": apellidoCoachee,
                            "NOMBRECOACH": nombreCoach,
                            "APELLIDOCOACH": apellidoCoach,
                            "IDSESION": canSesiones,
                            "ID": idProceso
                        }]
                        #se almacena una array de objetos
                        listados = json + listados
            #consulta de sesiones por proceso y usuarios
            for sCal in sesiones:
                #Descarta las sesiones Finalizadas y sin fecha 
                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                    for pCal in proceso:
                        #Descarta los procesos Finalizados
                        if pCal['ESTADOPROCESO_ID'] != 6:
                            for u in usuario:
                                #consulta por el usuario
                                if pCal['COACHEE_ID'] == u['ID']:
                                    #consulta por la id del proceso para traer las sesiones correspondientes
                                    if pCal['ID'] == sCal['PROCESO_ID']:
                                        fechaSesion = sCal['FECHASESION']
                                        estadoSesion = sCal['ESTADOSESION_ID']
                                        nombreEmpresa = pCal['NOMBREEMPRESA']
                                        nombreCoachee = u['NOMBRE']
                                        apellidoCoachee = u['APELLIDO']
                                        sesionId = sCal['ID']
                                        #se almacenan los datos en una variable
                                        sesionesCalendario2 = [{
                                            "NOMBREEMPRESA": nombreEmpresa,
                                            "NOMBRE": nombreCoachee,
                                            "APELLIDO": apellidoCoachee,
                                            "FECHASESION": fechaSesion,
                                            "ESTADOSESION_ID":estadoSesion,
                                            "ID": sesionId
                                        }]
                                        #se almacena una array de objetos
                                        sesionesCalendario3 = sesionesCalendario2 + sesionesCalendario3

            #consulta de sesiones por proceso
            for sBar in sesiones:
                for pBar in proceso:
                    if pBar['ID'] == sBar['PROCESO_ID']:
                        estadoSesion = sBar['ESTADOSESION_ID']
                        idSesion = sBar['ID']
                        #se almacenan los datos en una variable
                        sesionBarList = [{
                            "ID":idSesion,
                            "ESTADOSESION_ID":estadoSesion
                        }]
                        #se almacena una array de objetos
                        listadoBar = sesionBarList + listadoBar
                        #se ordena array por id de sesion de menor a mayor
                        listadoBarOrdenado = sorted(listadoBar, key=lambda k: k['ID'])

            #se obtiene la primera pagina del paginador
            page = request.GET.get('page', 1)

            try:
                #se le dan los atributos al paginador, listado de 4 por pagina
                paginator = Paginator(listados, 4)
                #se almacenan los resultados por por pagina
                listado = paginator.page(page)
            #si ocurre un error mostrara pagina no encontrada.
            except:
                raise Http404
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listado,
                'paginator': paginator,
                'sesiones': sesionesCalendario3,
                'listaBar': listadoBarOrdenado
            }
            #renderiza la vista y envia los datos
            return render(request, 'menu/menuCoachee.html', data)
        #si la consulta por perfil no corresponde redirige al usuario a su perfil en el menu principal
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            return redirect(plantilla)
    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')


#------------------------------Perteneciente al administrador-----------------------------------------------------
# --------------------------------  Paginas de Procesos ----------------------------------------------

#-------------------------------------------- Procesos admin Principal--------------------------------------------
def procesosAdmin(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&limit=5'
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstados = 'http://127.0.0.1:8001/estados-procesos'
            urlProcesosCal = 'http://127.0.0.1:8001/procesos?ESTADOPROCESO_ID!=4'
            urlSesionesCalendario = 'http://127.0.0.1:8001/sesiones'
            #obtiene los datos desde la api enviando token de seguridad
            proceso = requests.get(urlProcesos, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstados, headers=headers).json()
            sesionesCalendario = requests.get(urlSesionesCalendario, headers=headers).json()
            procesosCal = requests.get(urlProcesosCal, headers=headers).json()
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            sesionesCalendario3=[]
            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa = p['NOMBREEMPRESA']
                        nombreCoachee = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        correoCoachee = u['CORREO']
                        telefonoCoachee = u['FONO']
                        cantsesiones = p['CANTSESIONES']
                        fechaIni = p["FECHACREACION"]
                        objetivo = p['OBJETIVOS']
                        indicadores = p['INDICADORES']
                        planAccion = p['PLANACCION']
                        nombreJefe = u['NOMBREJEFE']
                        emailJefe = u['EMAILJEFE']
                        fonoJefe = u['FONOJEFE']
                        idProceso = p['ID']
                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE": nombreCoachee,
                            "APELLIDO": apellidoCoachee,
                            "CORREO": correoCoachee,
                            "FONO": telefonoCoachee,
                            "CANTSESIONES": cantsesiones,
                            "OBJETIVOS": objetivo,
                            "FECHACREACION": fechaIni,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,
                            "DESCRIPCION": estadoDescripcion,
                            "ID": idProceso
                        }]
                        #se almacena una array de objetos
                        listados = json + listados

            #consulta de sesiones por proceso y usuarios
            for sCal in sesionesCalendario:
                #Descarta las sesiones Finalizadas y sin fecha 
                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                    for pCal in procesosCal:
                        #Descarta los procesos Finalizados
                        if pCal['ESTADOPROCESO_ID'] != 6:
                            for u in usuario:
                                if pCal['COACHEE_ID'] == u['ID']:
                                    if pCal['ID'] == sCal['PROCESO_ID']:
                                        fechaSesion = sCal['FECHASESION']
                                        estadoSesion = sCal['ESTADOSESION_ID']
                                        nombreEmpresa = pCal['NOMBREEMPRESA']
                                        nombreCoachee = u['NOMBRE']
                                        apellidoCoachee = u['APELLIDO']
                                        #se almacenan los datos en una variable
                                        sesionesCalendario2 = [{
                                            "NOMBREEMPRESA": nombreEmpresa,
                                            "NOMBRE": nombreCoachee,
                                            "APELLIDO": apellidoCoachee,
                                            "FECHASESION": fechaSesion,
                                            "ESTADOSESION_ID":estadoSesion
                                        }]
                                        #se almacena una array de objetos
                                        sesionesCalendario3 = sesionesCalendario2 + sesionesCalendario3   

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listados,
                'sesiones': sesionesCalendario3
            }
            #renderiza la vista y envia los datos
            return render(request, 'procesos/procesosAdmin.html', data)
        #si la consulta por perfil no corresponde redirige al usuario a su perfil en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)
    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# --------------------------------------------Nuevo Proceso--------------------------------------------
def nuevoProceso(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlProcesosCal = 'http://127.0.0.1:8001/procesos?ESTADOPROCESO_ID!=4'
            urlSesionesCalendario = 'http://127.0.0.1:8001/sesiones'
            #obtiene los datos desde la api enviando token de seguridad
            usuario = requests.get(urlUsuarios, headers=headers).json()
            sesionesCalendario = requests.get(urlSesionesCalendario, headers=headers).json()
            procesosCal = requests.get(urlProcesosCal, headers=headers).json()
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            sesionesCalendario3=[]
            #consulta por el tipo de metodo y si el perfil corresponde al del administrador
            if request.method == 'POST' and perfil['perfil'] == 1:
                # Obtener datos del Front
                NOMBREEMPRESA = request.POST.get('nombreEmpre')
                CANTSESIONES = request.POST.get('cantiSesiones')
                OBJETIVOS = None
                INDICADORES = None
                PLANACCION = None
                ADMINISTRADOR_ID = '1'
                COACH_ID = request.POST.get('coachProces')
                COACHEE_ID = request.POST.get('coacheeProces')

                # Creo Json para enviar los datos a la api
                json = {
                    "NOMBREEMPRESA": NOMBREEMPRESA.title(),
                    "CANTSESIONES": CANTSESIONES,
                    "OBJETIVOS": OBJETIVOS,
                    "INDICADORES": INDICADORES,
                    "PLANACCION": PLANACCION,
                    "ADMINISTRADOR_ID": ADMINISTRADOR_ID,
                    "COACH_ID": COACH_ID,
                    "COACHEE_ID": COACHEE_ID
                }
                # Metodo para crear procesos en API
                url = 'http://127.0.0.1:8001/procesos'
                response = requests.post(url, headers=headers, json=json)
                #se consulta la respuesta de la api
                if response.status_code == 201:
                    # mensaje para avisar al front que se creo el proceso.
                    messages.success(request, 'Proceso creado con éxito.')
                    return redirect('nuevoProceso')
                else:
                    # si la respuesta no es de creado se muestra mensaje por pantalla
                    messages.error(
                        request, 'Hubo un problema al crear el proceso.')
                    return redirect('nuevoProceso')

            #consulta de sesiones por proceso y usuarios
            for sCal in sesionesCalendario:
                #Descarta las sesiones Finalizadas y sin fecha 
                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                    for pCal in procesosCal:
                        #Descarta los procesos Finalizados
                        if pCal['ESTADOPROCESO_ID'] != 6:
                            for u in usuario:
                                if pCal['COACHEE_ID'] == u['ID']:
                                    if pCal['ID'] == sCal['PROCESO_ID']:
                                        fechaSesion = sCal['FECHASESION']
                                        estadoSesion = sCal['ESTADOSESION_ID']
                                        nombreEmpresa = pCal['NOMBREEMPRESA']
                                        nombreCoachee = u['NOMBRE']
                                        apellidoCoachee = u['APELLIDO']

                                        #se almacenan los datos en una variable
                                        sesionesCalendario2 = [{
                                            "NOMBREEMPRESA": nombreEmpresa,
                                            "NOMBRE": nombreCoachee,
                                            "APELLIDO": apellidoCoachee,
                                            "FECHASESION": fechaSesion,
                                            "ESTADOSESION_ID":estadoSesion
                                        }]

                                        #se almacena una array de objetos
                                        sesionesCalendario3 = sesionesCalendario2 + sesionesCalendario3   

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'list_usuario': usuario,
                'sesiones': sesionesCalendario3
            }
            #renderiza la vista y envia los datos
            return render(request, 'procesos/nuevoProceso.html', data)
        #si la consulta por perfil no corresponde redirige al usuario a su perfil en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)
    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# --------------------------------------------listar Proceso--------------------------------------------

def buscaProceso(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID'
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstadosProcesos = 'http://127.0.0.1:8001/estados-procesos'
            #obtiene los datos desde la api enviando token de seguridad
            proceso = requests.get(urlProcesos, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstadosProcesos, headers=headers).json()
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa = p['NOMBREEMPRESA']
                        nombreCoachee = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        correoCoachee = u['CORREO']
                        telefonoCoachee = u['FONO']
                        fechaCreacion = p['FECHACREACION']
                        cantsesiones = p['CANTSESIONES']
                        objetivo = p['OBJETIVOS']
                        indicadores = p['INDICADORES']
                        planAccion = p['PLANACCION']
                        nombreJefe = u['NOMBREJEFE']
                        emailJefe = u['EMAILJEFE']
                        fonoJefe = u['FONOJEFE']
                        idProceso = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach = uc['NOMBRE']
                        apellidoCoach = uc['APELLIDO']

                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE": nombreCoachee,
                            "APELLIDO": apellidoCoachee,
                            "CORREO": correoCoachee,
                            "FONO": telefonoCoachee,
                            "FECHACREACION": fechaCreacion,
                            "CANTSESIONES": cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,
                            "DESCRIPCION": estadoDescripcion,
                            "NOMBRECOACH": nombreCoach,
                            "APELLIDOCOACH": apellidoCoach,
                            "ID": idProceso
                        }]

                        #se almacena una array de objetos
                        listados = json + listados

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listados,
            }
            #renderiza la vista y envia los datos
            return render(request, 'procesos/buscaProceso.html', data)
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)
    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# --------------------------------------------modificar Proceso--------------------------------------------

def modProceso(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #consulta por el tipo de metodo
            if request.method == 'POST':
                # Obtener datos del Front
                ID = id
                NOMBREEMPRESA = request.POST.get('nombreEmpresa')
                CANTSESIONES = request.POST.get('cantidadSesiones')
                FECHACREACION = request.POST.get('fechaCreacion')
                # TO DO esto se tiene que cambiar
                ADMINISTRADOR_ID = 1

                # Creo Json para enviar los datos a la api
                modificarProcesoJson = {
                    "ID": ID,
                    "NOMBREEMPRESA": NOMBREEMPRESA.title(),
                    "CANTSESIONES": CANTSESIONES,
                    "FECHACREACION": FECHACREACION,
                    "ADMINISTRADOR_ID": ADMINISTRADOR_ID,
                }

                # Metodo para modificar procesos en API
                modProceso = 'http://127.0.0.1:8001/procesos/' + str(id) + '/'
                response = requests.put(modProceso, json=modificarProcesoJson, headers=headers)
                #consulta respuesta de la api
                if response.status_code == 200:
                    # mensaje para avisar al front que se modifico el proceso.
                    messages.success(request, 'Proceso modificado con éxito.')
                    return redirect('buscaProceso')
                #si la respuesta de la api no es 200 de proceso modificado muestra mensaje
                else:
                    messages.error(
                        request, 'Hubo un problema al modificar el proceso.')
                    return redirect('buscaProceso')
            #redirecciona la vista a la lista de procesos
            return redirect('buscaProceso')
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)
    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# --------------------------------------------información Proceso--------------------------------------------

def visInfoProceso(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID=' + \
                str(id)
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstadosProcesos = 'http://127.0.0.1:8001/estados-procesos'
            urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)
            urlEstadoSesion = 'http://127.0.0.1:8001/estados-sesiones'
            #obtiene los datos desde la api enviando token de seguridad
            proceso = requests.get(urlProcesos, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstadosProcesos, headers=headers).json()
            sesiones = requests.get(urlSesiones, headers=headers).json()
            estadoSesion = requests.get(urlEstadoSesion, headers=headers).json()
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        idProcesoEstado = p['ESTADOPROCESO_ID']
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa = p['NOMBREEMPRESA']
                        nombreCoachee = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        correoCoachee = u['CORREO']
                        telefonoCoachee = u['FONO']
                        fechaCreacion = p['FECHACREACION']
                        cantsesiones = p['CANTSESIONES']
                        objetivo = p['OBJETIVOS']
                        indicadores = p['INDICADORES']
                        planAccion = p['PLANACCION']
                        nombreJefe = u['NOMBREJEFE']
                        emailJefe = u['EMAILJEFE']
                        fonoJefe = u['FONOJEFE']
                        idProceso = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach = uc['NOMBRE']
                        apellidoCoach = uc['APELLIDO']

                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE": nombreCoachee,
                            "APELLIDO": apellidoCoachee,
                            "CORREO": correoCoachee,
                            "FONO": telefonoCoachee,
                            "FECHACREACION": fechaCreacion,
                            "CANTSESIONES": cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,
                            "DESCRIPCION": estadoDescripcion,
                            "NOMBRECOACH": nombreCoach,
                            "APELLIDOCOACH": apellidoCoach,
                            "ID": idProceso,
                            "IDESTADOPROCESO": idProcesoEstado
                        }]

                        #se almacena una array de objetos
                        listados = json + listados
            # TO DO esto me parece que esta demas
            sesiones = sesiones
            estadoSesion = estadoSesion

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listados,
                'sesiones': sesiones,
                'estadosSesion': estadoSesion
            }

            #renderiza la vista y envia los datos
            return render(request, 'procesos/visInfoProceso.html', data)

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# --------------------------------------------Finalizar un proceso Administrador--------------------------------------------

def finProceso(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos/'+str(id)+'/'
            #variable que almacena el dia actual
            day = datetime.today().strftime('%Y-%m-%d')

            #se almacenan los datos del proceso a finalizar en una variable
            finProcesoJson = {
                "ID": id,
                "FECHATERMINO": day,
                "ACTIVO": 0,
                "ESTADOPROCESO_ID": 6
            }

            #metodo que modificara el estado del proceso 
            response = requests.put(urlProcesos, json=finProcesoJson, headers=headers)
           
            #consulta respuesta de la api
            if response.status_code == 200:
                # mensaje para avisar al front que se modifico el proceso.
                messages.success(request, 'Proceso finalizado con éxito.')
                return redirect('buscaProceso')

            #respuesta de la api en caso de no encontrar la id del proceso
            elif response.status_code == 404:
                messages.warning(request, 'El proceso ya está finalizado.')
                return redirect('buscaProceso')
            
            #si se entrega otra respuesta diferente a las anteriores muestra este mensaje de error
            else:
                messages.error(
                    request, 'Hubo un problema al finalizar el proceso.')
                return redirect('buscaProceso')

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')


# ----------------------------------- USUARIOS ------------------------------------------

# --------------------------------------------usuarios admin Principal--------------------------------------------
def usuariosAdmin(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            urlCoach = 'http://127.0.0.1:8001/usuarios?ordering=-ID&limit=5&PERFIL_ID=2'
            urlCoachee = 'http://127.0.0.1:8001/usuarios?ordering=-ID&limit=5&PERFIL_ID=3'

            #obtiene los datos desde la api enviando token de seguridad
            list_coachs = requests.get(urlCoach, headers=headers).json()
            list_coachees = requests.get(urlCoachee, headers=headers).json()

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'list_coachs': list_coachs,
                'list_coachees': list_coachees
            }

            #renderiza la vista y envia los datos
            return render(request, 'usuarios/usuariosAdmin.html', data)
        
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')


# --------------------------------------------nuevo usuario--------------------------------------------
def nuevoUsuario(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            # Crear usuario
            if request.method == 'POST' and perfil['perfil'] == 1:
                # Obtener datos del Front
                APELLIDO = request.POST.get('apellido')
                CORREO = request.POST.get('email')
                FONO = request.POST.get('telefono')
                IDIOMA = request.POST.get('idioma')
                # Se definen por defecto en None
                EMPRESA = ""
                NOMBREJEFE = ""
                APELLIDOJEFE = ""
                EMAILJEFE = ""
                FONOJEFE = ""
                # Por defecto Activo
                ACTIVO = 1
                # Obtiene tipo de usuario
                if 'nombreCoachee' in request.POST:
                    # Asigno Perfil
                    PERFIL_ID = 3
                    NOMBRE = request.POST.get('nombreCoachee')
                    EMPRESA = request.POST.get('nombreEmp')
                    NOMBREJEFE = request.POST.get('nombreJefe')
                    APELLIDOJEFE = request.POST.get('apellidoJefe')
                    EMAILJEFE = request.POST.get('emailJefe')
                    FONOJEFE = request.POST.get('telefonoJefe')

                elif 'nombreCoach' in request.POST:
                    # Asigno Perfil
                    PERFIL_ID = 2
                    NOMBRE = request.POST.get('nombreCoach')

                else:
                    # Usuario Administrador
                    # Asigno Perfil
                    PERFIL_ID = 1
                    NOMBRE = request.POST.get('nombreAdmin')

                # Creo Json
                crearUsuariosJson = {
                    "CORREO": CORREO,
                    "NOMBRE": NOMBRE,
                    "APELLIDO": APELLIDO,
                    "FONO": FONO,
                    "IDIOMA": IDIOMA,
                    "EMPRESA": EMPRESA,
                    "NOMBREJEFE": str(NOMBREJEFE)+' '+str(APELLIDOJEFE),
                    "EMAILJEFE": EMAILJEFE,
                    "FONOJEFE": FONOJEFE,
                    "ACTIVO": ACTIVO,
                    "PERFIL_ID": PERFIL_ID
                }

                # Metodo para crear usuario en API
                urlCrearUsuarios = 'http://127.0.0.1:8001/usuarios'
                response = requests.post(urlCrearUsuarios, headers=headers, json=crearUsuariosJson)

                #se almacenan las variables con los datos en un objeto para enviarlo a la vista
                data = {
                    'usuario': perfil
                }
                #se consulta la respuesta de la api
                if response.status_code == 201:
                    # mensaje para mostrar por vista que se creo el usuario.
                    messages.success(request, 'Usuario creado con éxito.')
                    return render(request, 'usuarios/nuevoUsuario.html', data)
                # mensaje para mostrar por la vista que el usuario no se creo.
                else:
                    messages.error(request, 'Hubo un problema al crear el usuario.')
            

            #renderiza la vista y envia los datos
            return render(request, 'usuarios/nuevoUsuario.html', data)

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# ----------------------------------lista usuario---------------------------------------------------

def listUsuarios(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            
            #variable que almacena la url de la api
            urlListarUsuarios = 'http://127.0.0.1:8001/usuarios'

            #obtiene los datos desde la api enviando token de seguridad
            usuarios = requests.get(urlListarUsuarios, headers=headers).json()

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': usuarios,
            }

            #renderiza la vista y envia los datos
            return render(request, 'usuarios/listUsuarios.html', data)
        
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')


# ----------------------------------Modifica usuario----------------------------------
def modUsuarios(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #consulta metodo
            if request.method == 'POST':
                # Obtener datos del Front
                APELLIDO = request.POST.get('apellido')
                CORREO = request.POST.get('email')
                FONO = request.POST.get('telefono')
                IDIOMA = request.POST.get('idioma')
                # Se definen por defecto en None
                EMPRESA = None
                NOMBREJEFE = None
                EMAILJEFE = None
                FONOJEFE = None
                # Por defecto Activo
                estado = request.POST.get('activo')
                if 'activo' in request.POST:
                    ACTIVO = 1
                else:
                    ACTIVO = 0

                # Obtiene tipo de usuario
                if 'nombreCoachee' in request.POST:
                    # Asigno Perfil
                    PERFIL_ID = 3
                    NOMBRE = request.POST.get('nombreCoachee')
                    EMPRESA = request.POST.get('nombreEmp')
                    NOMBREJEFE = request.POST.get('nombrejefe')
                    EMAILJEFE = request.POST.get('emailjefe')
                    FONOJEFE = request.POST.get('telefonoJefe')

                elif 'nombreCoach' in request.POST:
                    # Asigno Perfil
                    PERFIL_ID = 2
                    NOMBRE = request.POST.get('nombreCoach')

                else:
                    # Usuario Administrador
                    # Asigno Perfil
                    PERFIL_ID = 1
                    NOMBRE = request.POST.get('nombreAdmin')

                # Creo Json
                modificaUsuarioJson = {
                    "ID": id,
                    "CORREO": CORREO,
                    "NOMBRE": NOMBRE,
                    "APELLIDO": APELLIDO,
                    "FONO": FONO,
                    "IDIOMA": IDIOMA,
                    "EMPRESA": EMPRESA,
                    "NOMBREJEFE": str(NOMBREJEFE),
                    "EMAILJEFE": EMAILJEFE,
                    "FONOJEFE": FONOJEFE,
                    "ACTIVO": ACTIVO,
                    "PERFIL_ID": PERFIL_ID
                }

                # Metodo para modificar usuario en API
                urlModUsuarios = 'http://127.0.0.1:8001/usuarios/' + \
                    str(id) + '/'
                response = requests.put(urlModUsuarios, headers=headers, json=modificaUsuarioJson)
                
                #consulta respuesta de la api
                if response.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Usuario actualizado con éxito.')
                    return redirect('listUsuarios')

                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    messages.error(
                        request, 'Hubo un problema al actualizar el usuario.')
                    return redirect('listUsuarios')

            #usuario es redirigido a la lista de usuarios
            return redirect('listUsuarios')
        
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

# ------------------------ Perteneciente al Coach ------------------------------

# ----------------------------------listar Proceso Coach----------------------------------
def listProCoach(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al coach
        if perfil['perfil'] == 2:
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&COACH_ID=' + \
                str(perfil['id'])
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            
            #obtiene los datos desde la api enviando token de seguridad
            proceso = requests.get(urlProcesos, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstado, headers=headers).json()

            #variable que almacenara el listado de procesos y sus datos
            listados = []

            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa = p['NOMBREEMPRESA']
                        nombreCoachee = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        correoCoachee = u['CORREO']
                        telefonoCoachee = u['FONO']
                        fechaCreacion = p['FECHACREACION']
                        cantsesiones = p['CANTSESIONES']
                        objetivo = p['OBJETIVOS']
                        indicadores = p['INDICADORES']
                        planAccion = p['PLANACCION']
                        nombreJefe = u['NOMBREJEFE']
                        emailJefe = u['EMAILJEFE']
                        fonoJefe = u['FONOJEFE']
                        idProceso = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach = uc['NOMBRE']
                        apellidoCoach = uc['APELLIDO']

                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE": nombreCoachee,
                            "APELLIDO": apellidoCoachee,
                            "CORREO": correoCoachee,
                            "FONO": telefonoCoachee,
                            "FECHACREACION": fechaCreacion,
                            "CANTSESIONES": cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,
                            "DESCRIPCION": estadoDescripcion,
                            "NOMBRECOACH": nombreCoach,
                            "APELLIDOCOACH": apellidoCoach,
                            "ID": idProceso
                        }]

                        #se almacena una array de objetos
                        listados = json + listados

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listados,
            }

            #renderiza la vista y envia los datos
            return render(request, 'procesoCoach/listProCoach.html', data)

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')


# ----------------------------------Procesos asignados al Coach----------------------------------
def procAsig(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al coach
        if perfil['perfil'] == 2:
            #variable que almacena la url de la api
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ESTADOPROCESO_ID=1&COACH_ID=' + \
                str(perfil['id'])
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'

            #obtiene los datos desde la api enviando token de seguridad
            proceso = requests.get(urlProcesos, headers=headers).json()
            usuario = requests.get(urlUsuarios, headers=headers).json()
            estado = requests.get(urlEstado, headers=headers).json()

            #variable que almacenara el listado de procesos y sus datos
            listados = []

            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa = p['NOMBREEMPRESA']
                        nombreCoachee = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        correoCoachee = u['CORREO']
                        telefonoCoachee = u['FONO']
                        fechaCreacion = p['FECHACREACION']
                        cantsesiones = p['CANTSESIONES']
                        objetivo = p['OBJETIVOS']
                        indicadores = p['INDICADORES']
                        planAccion = p['PLANACCION']
                        nombreJefe = u['NOMBREJEFE']
                        emailJefe = u['EMAILJEFE']
                        fonoJefe = u['FONOJEFE']
                        idProceso = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach = uc['NOMBRE']
                        apellidoCoach = uc['APELLIDO']

                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE": nombreCoachee,
                            "APELLIDO": apellidoCoachee,
                            "CORREO": correoCoachee,
                            "FONO": telefonoCoachee,
                            "FECHACREACION": fechaCreacion,
                            "CANTSESIONES": cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,
                            "DESCRIPCION": estadoDescripcion,
                            "NOMBRECOACH": nombreCoach,
                            "APELLIDOCOACH": apellidoCoach,
                            "ID": idProceso
                        }]

                        #se almacena una array de objetos
                        listados = json + listados

            #se obtiene la primera pagina del paginador
            page = request.GET.get('page', 1)

            try:
                #se le dan los atributos al paginador, listado de 10 por pagina
                paginator = Paginator(listados, 10)
                #se almacenan los resultados por por pagina
                listado = paginator.page(page)
            #si ocurre un error mostrara pagina no encontrada.
            except:
                raise Http404

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listado,
                'paginator': paginator
            }

            #renderiza la vista y envia los datos
            return render(request, 'procesoCoach/procAsig.html', data)

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

#---------------------------------- Obtener y modificar de los procesos coach----------------------------------
def infoProCoach(request, id):
    #try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al coach
        if perfil['perfil'] == 2:
            #consulta metodo
            if request.method == 'POST':
                objetivo = request.POST.get('objetivosProc')
                indicadores = request.POST.get('indicadoresProc')
                planAccion = request.POST.get('planAccionProc')
                estadoProceso = request.POST.get('estadoProceso')
                idProceso = id
                #se almacenan los datos en una variable
                modProcCoach = {
                    "ID": idProceso,
                    "OBJETIVOS": objetivo,
                    "INDICADORES": indicadores,
                    "PLANACCION": planAccion,
                    "ESTADOPROCESO_ID": estadoProceso
                }

                # Metodo para modificar proceso Coach en API
                urlModProcesos = 'http://127.0.0.1:8001/procesos/' + str(id) + '/'
                response = requests.put(urlModProcesos, headers=headers, json=modProcCoach)

                #consulta respuesta de la api
                if response.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Proceso actualizado con éxito.')
                    return redirect('infoProCoach', id)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    messages.error(
                        request, 'Hubo un problema al actualizar el proceso.')
                    return redirect('infoProCoach', id)
            
            #consulta metodo
            if request.method == 'GET':
                #variable que almacena la url de la api
                urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID=' + \
                    str(id)
                urlUsuarios = 'http://127.0.0.1:8001/usuarios'
                urlEstado = 'http://127.0.0.1:8001/estados-procesos'
                urlEstadoSesion = 'http://127.0.0.1:8001/estados-sesiones'
                urlGestorArchivo = 'http://127.0.0.1:8001/gestor-archivo'
                urlEnlace = 'http://127.0.0.1:8001/enlaces'

                #obtiene los datos desde la api enviando token de seguridad
                proceso = requests.get(urlProcesos, headers=headers).json()
                usuario = requests.get(urlUsuarios, headers=headers).json()
                estado = requests.get(urlEstado, headers=headers).json()
                gestorArchivo = requests.get(urlGestorArchivo, headers=headers).json()
                enlace = requests.get(urlEnlace, headers=headers).json()
                urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)
                sesiones = requests.get(urlSesiones, headers=headers).json()
                estadoSesion = requests.get(urlEstadoSesion, headers=headers).json()
                gestorArchivo = requests.get(urlGestorArchivo, headers=headers).json()
                enlace = requests.get(urlEnlace, headers=headers).json()

                #variable que almacenara el listado de procesos y sus datos
                listados = []

                #variable que almacenara el listado de archivos
                gestorArchivoJson = []
                gestorEnlaceJson = []

                #consulta de procesos por estadoproceso y usuarios
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID'] == e['ID']:
                            idProcesoEstado = p['ESTADOPROCESO_ID']
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID'] == u['ID']:
                            nombreEmpresa = p['NOMBREEMPRESA']
                            nombreCoachee = u['NOMBRE']
                            apellidoCoachee = u['APELLIDO']
                            correoCoachee = u['CORREO']
                            telefonoCoachee = u['FONO']
                            fechaCreacion = p['FECHACREACION']
                            cantsesiones = p['CANTSESIONES']
                            objetivo = p['OBJETIVOS']
                            indicadores = p['INDICADORES']
                            planAccion = p['PLANACCION']
                            nombreJefe = u['NOMBREJEFE']
                            emailJefe = u['EMAILJEFE']
                            fonoJefe = u['FONOJEFE']
                            idProceso = p['ID']
                    for uc in usuario:
                        if p['COACH_ID'] == uc['ID']:
                            nombreCoach = uc['NOMBRE']
                            apellidoCoach = uc['APELLIDO']

                            #se almacenan los datos en una variable
                            json = [{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE": nombreCoachee,
                                "APELLIDO": apellidoCoachee,
                                "CORREO": correoCoachee,
                                "FONO": telefonoCoachee,
                                "FECHACREACION": fechaCreacion,
                                "CANTSESIONES": cantsesiones,
                                "OBJETIVOS": objetivo,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,
                                "DESCRIPCION": estadoDescripcion,
                                "NOMBRECOACH": nombreCoach,
                                "APELLIDOCOACH": apellidoCoach,
                                "ID": idProceso,
                                "IDESTADOPROCESO": idProcesoEstado
                            }]

                            #se almacena una array de objetos
                            listados = json + listados

                #consulta para obtener la id de los archivos y links asociados a la sesion
                for s in sesiones:
                    for g in gestorArchivo:
                        if s['ID'] == g['SESION_ID']:
                            linkGestor = g['LINK']

                            jsonLG = [{
                                    "IDLINKGE": g['SESION_ID'],
                                    "LINKGE": linkGestor
                                }]
                            
                            gestorArchivoJson = jsonLG + gestorArchivoJson
                print(gestorArchivoJson)
                
                for s in sesiones:
                    for en in enlace:
                        if s['ID'] == en['SESION_ID']:
                            linkEnlace = en['LINK']  
                            
                            jsonLE = [{
                                    "IDLINKEN": en['SESION_ID'],
                                    "LINKEN": linkEnlace
                                }]

                            #se almacena una array de objetos
                            gestorEnlaceJson = jsonLE + gestorEnlaceJson
                print(gestorEnlaceJson)

                # TO DO esto creo que esta demas
                sesiones = sesiones
                estado = estado
                estadoSesion = estadoSesion
                
                #se almacenan las variables con los datos en un objeto para enviarlo a la vista
                data = {
                    'usuario': perfil,
                    'entity': listados,
                    'sesiones': sesiones,
                    'estados': estado,
                    'estadosSesion': estadoSesion,
                    'gestoresEnlaces': gestorEnlaceJson,
                    'gestoresArchivos': gestorArchivoJson
                }

                #renderiza la vista y envia los datos
                return render(request, 'procesoCoach/infoProCoach.html', data)
        
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
 #   except Exception as e:
  #      messages.warning(request,'Ingrese sus credenciales para acceder')
   #     return redirect('/')

# ----------------------------------Modificar sesiones Coach----------------------------------
def infoSesionCoach(request, id):
#    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        
        #se consulta si el perfil de usuario corresponde al coach
        if perfil['perfil'] == 2:
            #se obtiene dato desde la vista
            idP = request.POST.get('proceso')
            #consulta metodo a utilizar
            if request.method == 'POST':
                #idP =  request.POST.get('proceso')
                FECHASESION = request.POST.get('fechaSesion')
                HORASESION = request.POST.get('horaSesion')
                DESCRIPCION = request.POST.get('descSesion')
                AVANCES = request.POST.get('avancesSesion')
                ASIGNACION = request.POST.get('asigSesion')
                ESTADOSESION_ID = request.POST.get('estadoSesion1')
                archivo = request.FILES.get('archivo')
                link = request.POST.get('link')

                #se almacenan los datos en una variable
                modificarSesionesJson = {
                    "ID": id,
                    "FECHASESION": FECHASESION,
                    "HORASESION": HORASESION,
                    "DESCRIPCION": DESCRIPCION,
                    "AVANCES": AVANCES,
                    "ASIGNACION": ASIGNACION,
                    "PROCESO_ID": idP,
                    "ESTADOSESION_ID": ESTADOSESION_ID
                }

                gestorEnlace = {
                    "LINK": link,
                    "SESION_ID": id
                }

                gestorArchivo = {
                    "LINK": archivo,
                    "SESION_ID": id,
                    "TIPOARCHIVO_ID": 1
                }

                #metodo para modificar sesion
                urlSesiones = 'http://127.0.0.1:8001/sesiones/'+str(id)+'/'
                response = requests.put(urlSesiones, headers=headers, json=modificarSesionesJson)

                #metodo para modificar sesion
                urlArchivos = 'http://127.0.0.1:8001/gestor-archivo'
                responseArchivo = requests.put(urlArchivos, headers=headers, json=gestorArchivo)

                #metodo para modificar sesion
                urlEnlaces = 'http://127.0.0.1:8001/enlaces'
                responseEnlaces = requests.post(urlEnlaces, headers=headers, json=gestorEnlace)
                
                #print('archivo', gestorArchivo, archivo )
                #consulta respuesta de la api
                if response.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Sesión actualizada con éxito.')
                    return redirect('infoProCoach', idP)
                    #consulta respuesta de la api
                elif responseArchivo.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Archivos almacenados con éxito.')
                    return redirect('infoProCoach', idP)
                elif responseEnlaces.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Enlaces almacenado con éxito.')
                    return redirect('infoProCoach', idP)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    # se reemplazan comillas dobles que trae el mensaje desde la api
                    messages.error(
                        request, response.text.replace('"', ''))
                    return redirect('infoProCoach', idP)

            #redirecciona la vista terminado el metodo 
            return redirect('listProCoach')

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 3:
                plantilla = 'menuCoachee'
            return redirect(plantilla)
    
    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
#    except Exception as e:
#        messages.warning(request,'Ingrese sus credenciales para acceder')
#        return redirect('/')

# ------------------------------  Perteneciente al Coachee ----------------------------------------------#

# ----------------------------------Procesos asignados al Coachee----------------------------------
def infoProCoachee(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al coachee
        if perfil['perfil'] == 3:
            #consulta metodo a utilizar
            if request.method == 'GET':
                #variable que almacena la url de la api
                urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID=' + \
                    str(id)
                urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)
                urlUsuarios = 'http://127.0.0.1:8001/usuarios'
                urlEstado = 'http://127.0.0.1:8001/estados-procesos'
                urlEstadoSesion = 'http://127.0.0.1:8001/estados-sesiones'
                urlGestorArchivo = 'http://127.0.0.1:8001/gestor-archivo'
                urlEnlace = 'http://127.0.0.1:8001/enlaces'

                #obtiene los datos desde la api enviando token de seguridad
                proceso = requests.get(urlProcesos, headers=headers).json()
                usuario = requests.get(urlUsuarios, headers=headers).json()
                estado = requests.get(urlEstado, headers=headers).json()
                sesiones = requests.get(urlSesiones, headers=headers).json()
                estadoSesion = requests.get(urlEstadoSesion, headers=headers).json()
                gestorArchivo = requests.get(urlGestorArchivo, headers=headers).json()
                enlace = requests.get(urlEnlace, headers=headers).json()

                #variable que almacenara el listado de procesos y sus datos
                listados = []
                #variable que almacenara los archivos de las sesiones
                gestorEnlace = []

                #consulta de procesos por estadoproceso y usuarios
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID'] == e['ID']:
                            idProcesoEstado = p['ESTADOPROCESO_ID']
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID'] == u['ID']:
                            nombreEmpresa = p['NOMBREEMPRESA']
                            nombreCoachee = u['NOMBRE']
                            apellidoCoachee = u['APELLIDO']
                            correoCoachee = u['CORREO']
                            telefonoCoachee = u['FONO']
                            fechaCreacion = p['FECHACREACION']
                            cantsesiones = p['CANTSESIONES']
                            objetivo = p['OBJETIVOS']
                            indicadores = p['INDICADORES']
                            planAccion = p['PLANACCION']
                            nombreJefe = u['NOMBREJEFE']
                            emailJefe = u['EMAILJEFE']
                            fonoJefe = u['FONOJEFE']
                            idProceso = p['ID']
                    for uc in usuario:
                        if p['COACH_ID'] == uc['ID']:
                            nombreCoach = uc['NOMBRE']
                            apellidoCoach = uc['APELLIDO']

                            #se almacenan los datos en una variable
                            json = [{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE": nombreCoachee,
                                "APELLIDO": apellidoCoachee,
                                "CORREO": correoCoachee,
                                "FONO": telefonoCoachee,
                                "FECHACREACION": fechaCreacion,
                                "CANTSESIONES": cantsesiones,
                                "OBJETIVOS": objetivo,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,
                                "DESCRIPCION": estadoDescripcion,
                                "NOMBRECOACH": nombreCoach,
                                "APELLIDOCOACH": apellidoCoach,
                                "IDESTADOPROCESO": idProcesoEstado,
                                "ID": idProceso
                            }]

                            #se almacena una array de objetos
                            listados = json + listados

                #consulta para obtener la id de los archivos y links asociados a la sesion
                for s in sesiones:
                    for g in gestorArchivo:
                        if s['ID'] == g['SESION_ID']:
                            idLinkGestor = g['SESION_ID']
                            linkGestor = g['LINK']
                    for en in enlace:
                        if s['ID'] == en['SESION_ID']:
                            idlinkEnlace = en['SESION_ID']
                            linkEnlace = en['LINK']   
                            jsonGE = [{
                                "IDLINKGE": idlinkEnlace,
                                "LINKGE": linkGestor,
                                "IDLINKEN": idlinkEnlace,
                                "LINKEN": linkEnlace
                            }]

                            #se almacena una array de objetos
                            gestorEnlace = jsonGE + gestorEnlace

                # TO DO esto creo que esta demas
                sesiones = sesiones
                estado = estado
                estadoSesion = estadoSesion

                #se almacenan las variables con los datos en un objeto para enviarlo a la vista
                data = {
                    'usuario': perfil,
                    'entity': listados,
                    'sesiones': sesiones,
                    'estados': estado,
                    'estadosSesion': estadoSesion,
                    'gestores':gestorEnlace
                }

                #renderiza la vista de informacion de procesos coachee y envia los datos a esta
                return render(request, 'procesoCoachee/infoProCoachee.html', data)
        
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

# ----------------------------------Imprimi Reporte----------------------------------
def imprimirProceso(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al coach o administrador
        #if perfil['perfil'] == 2 or perfil['perfil'] == 1:

        #variable que almacena la url de la api
        urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID=' + \
            str(id)
        urlUsuarios = 'http://127.0.0.1:8001/usuarios'
        urlEstado = 'http://127.0.0.1:8001/estados-procesos'
        urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)

        #obtiene los datos desde la api enviando token de seguridad
        proceso = requests.get(urlProcesos, headers=headers).json()
        usuario = requests.get(urlUsuarios, headers=headers).json()
        estado = requests.get(urlEstado, headers=headers).json()
        sesiones = requests.get(urlSesiones, headers=headers).json()

        #variable que almacenara el listado de procesos y sus datos
        listados = []

        #consulta de procesos por estadoproceso y usuarios
        for p in proceso:
            for e in estado:
                if p['ESTADOPROCESO_ID'] == e['ID']:
                    estadoDescripcion = e['DESCRIPCION']
            for u in usuario:
                if p['COACHEE_ID'] == u['ID']:
                    nombreEmpresa = p['NOMBREEMPRESA']
                    nombreCoachee = u['NOMBRE']
                    apellidoCoachee = u['APELLIDO']
                    correoCoachee = u['CORREO']
                    telefonoCoachee = u['FONO']
                    fechaCreacion = p['FECHACREACION']
                    fechaTermino = p['FECHATERMINO']
                    cantsesiones = p['CANTSESIONES']
                    objetivo = p['OBJETIVOS']
                    indicadores = p['INDICADORES']
                    planAccion = p['PLANACCION']
                    nombreJefe = u['NOMBREJEFE']
                    emailJefe = u['EMAILJEFE']
                    fonoJefe = u['FONOJEFE']
                    idProceso = p['ID']
            for uc in usuario:
                if p['COACH_ID'] == uc['ID']:
                    nombreCoach = uc['NOMBRE']
                    apellidoCoach = uc['APELLIDO']
                    correoCoach = uc['CORREO']
                    fonoCoach = uc['FONO']

                    #se almacenan los datos en una variable
                    json = [{
                        "NOMBREEMPRESA": nombreEmpresa,
                        "NOMBRE": nombreCoachee,
                        "APELLIDO": apellidoCoachee,
                        "CORREO": correoCoachee,
                        "FONO": telefonoCoachee,
                        "FECHACREACION": fechaCreacion,
                        "FECHATERMINO": fechaTermino,
                        "CANTSESIONES": cantsesiones,
                        "OBJETIVOS": objetivo,
                        "INDICADORES": indicadores,
                        "PLANACCION": planAccion,
                        "NOMBREJEFE": nombreJefe,
                        "EMAILJEFE": emailJefe,
                        "FONOJEFE": fonoJefe,
                        "DESCRIPCION": estadoDescripcion,
                        "NOMBRECOACH": nombreCoach,
                        "APELLIDOCOACH": apellidoCoach,
                        "CORREOCOACH": correoCoach,
                        "FONOCOACH": fonoCoach,
                        "ID": idProceso
                    }]

                    #se almacena una array de objetos
                    listados = json + listados

        #se obtine diseño de pdf
        template = get_template("base/reporte.html")

        #se almacena datos que iran al pdf
        context = {
            'entity': listados,
            'sesiones': sesiones
        }

        # se cargan datos dentro del diseño del pdf y se agregan los estilos a este
        html_template = template.render(context)
        css_url = os.path.join(settings.BASE_DIR, 'frontProject/static/css/bootstrap.css')

        #se obtiene el pdf
        pdf_file = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])

        #al httpresponse se le entrega el pdf y se le indica que tipo de archivo
        response = HttpResponse(pdf_file, content_type='application/pdf;')

        #aca se le asi
        #response['Content-Disposition'] = 'inline; filename=reporte_proceso.pdf'

        #transforma la informacion en binaria
        encoded = base64.b64encode(pdf_file)

        #tipo de transferencia
        response['Content-Transfer-Encoding'] = 'binary'

        #se le asigna el nombre al pdf
        response['Content-Disposition'] = 'attachment; filename= ReporteEmpresa_' + \
            nombreEmpresa + '.pdf'

        #retorna el pdf
        return response

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal
        # else:
        #     if perfil['perfil'] == 1:
        #         plantilla = 'menuAdmin'
        #     elif perfil['perfil'] == 3:
        #         plantilla = 'menuCoachee'
        #     return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')


# ---------------------- modificar plan de accion coachee----------
def modPlanAccion(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al coachee
        if perfil['perfil'] == 3:
            #consulta metodo a utilizar
            if request.method == 'POST':
                #se toma id de proceso que envia la vista
                IDp = id
                #se obtine el plan de acciondesde la vista y se almacena en variable
                PLANDEACCION = request.POST.get('planAccionProc')
                #se almacenan los datos en variable
                modificarPlanJson = {
                    "ID": IDp,
                    "PLANACCION": PLANDEACCION
                }
                #metodo para actualizar plan de accion
                modPlanAccion = 'http://127.0.0.1:8001/procesos/' + \
                    str(id) + '/'
                response = requests.put(modPlanAccion, json=modificarPlanJson, headers=headers)

                #consulta respuesta de la api
                if response.status_code == 200:
                    # mensaje para avisar al front que se modifico el proceso.
                    messages.success(
                        request, 'Plan de acción modificado con éxito.')
                    return redirect('infoProCoachee', IDp)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    messages.error(
                        request, 'Hubo un problema al modificar el Plan de Acción.')
                    return redirect('infoProCoachee', IDp)
            #redirecciona a la informacion de proceso de coachee
            return redirect('infoProCoachee')

        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal  
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            return redirect(plantilla)

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

#----------------------------------modificar avances de sesiones ----------------------------------
def modSesionAvance(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']

        #se consulta si el perfil de usuario corresponde al coachee
        if perfil['perfil'] == 3:
            #se obtiene metodo a utilizar
            if request.method == 'POST':
                #se toma id de sesion que envia la vista
                IDs = id
                #se almacena id de proceso desde la vista
                idp = request.POST.get('proceso')
                #se obtine respuesta avances de sesion desde la vista y se almacena en variable
                RESPUESTA = request.POST.get('respuestaAvancesSesion')
                #se almacenan los datos en variable
                modificarRespAvancesJson = {
                    "ID": int(IDs),
                    "PROCESO_ID":int(idp),
                    "RESPUESTA": RESPUESTA
                }
                #metodo para actualizar
                modRespAvances = 'http://127.0.0.1:8001/sesiones/' + \
                    str(id) + '/'
                response = requests.put(modRespAvances, json=modificarRespAvancesJson, headers=headers)
                
                #consulta respuesta de la api
                if response.status_code == 200:
                    # mensaje para avisar al front que se actualizo respuesta avances.
                    messages.success(
                        request, 'Estado de avances actualizado con éxito.')
                    return redirect('infoProCoachee', idp)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    messages.error(
                        request, 'Hubo un problema al modificar el Estado de Avances.')
                    return redirect('infoProCoachee', idp)
            #redirecciona a la informacion de proceso de coachee
            return redirect('infoProCoachee')
        #si la consulta por perfil no corresponde redirige al usuario a su perfil correspondiente en el menu principal  
        else:
            if perfil['perfil'] == 1:
                plantilla = 'menuAdmin'
            elif perfil['perfil'] == 2:
                plantilla = 'menuCoach'
            return redirect(plantilla)
    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')