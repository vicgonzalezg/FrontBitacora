#se importan librerias
import base64
from django.shortcuts           import render, redirect
from django.http                import HttpResponse, Http404
from django.core.paginator      import Paginator
from django.template.loader     import get_template
from bitacoraProject.wsgi       import *
from django.contrib             import messages
from weasyprint                 import HTML, CSS
from datetime                   import datetime
from .services                  import *
from bitacoraProject.settings   import BASE_DIR
# --------------------------------------------definimos el login--------------------------------------------
def login(request):
    if request.method == 'POST':
        #obtenemos credenciales desde formulario html
        r = UsuarioPublicoAPICall.login(request)
        #consultamos por respuesta servidor
        if r.status_code == 200:
            perfil_usuario=sesionUsuario(request,r)
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
            r.encoding = 'utf-8'
            messages.error(request, r.text.replace('"', ''))
            return render(request, 'login/login.html')
    #renderiza la vista de login
    return render(request, 'login/login.html')

#--------------------------------------------Recuperar Contraseña--------------------------------------------
def recuperarClave(request):
    if request.method == 'POST':
        response = UsuarioPublicoAPICall.recuperacionContrasena(request)
        if response.status_code == 200:
            messages.success(request, 'Se enviara un correo con las instrucciones.')
        else:
            response.encoding = 'utf-8'
            messages.error(request, response.text.replace('"', ''))

    return  render(request, 'login/recuperarClave.html')

#-------------------------------------------- Cambio de Contraseña--------------------------------------------
def cambioclave(request, pk):
    if request.method == 'POST':
        response = UsuarioPublicoAPICall.validacionRecuperacionContrasena(request,pk)
        if response.status_code == 200:
            messages.success(request, 'Contraseña cambiada con éxito. Seras redirigido al Login.')
        else:
            response.encoding = 'utf-8'
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

    """
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
    """

# --------------------------------------------Perfil de usuarios--------------------------------------------
def perfil(request):
    try:

        usuario = UsuariosAPICall.get(request,None)

        data = {
            'usuario':  perfilUsuario(request),
            'entity' :  usuario,
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
        perfil = perfilUsuario(request)
        #se consulta si el prefin de usuario corresponde al de administrador
        if perfil['perfil'] == 1:
            #obtiene los datos desde la api enviando token de seguridad
            queryProcesos       ='ordering=-ID&limit=5'
            queryProcesosCal    = 'ACTIVO=1'
            procesos            = ProcesosAPICall.get(request,queryProcesos)
            usuarios            = UsuariosAPICall.get(request, None)
            estados             = EstadosProcesosAPICall.get(request,None)
            procesosCal         = ProcesosAPICall.get(request,queryProcesosCal)
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            listadoProcesosOrdenados = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            listadoSesionesCalendario = []
            
            #consulta de procesos por estado y usuarios
            for p in procesos:
                for e in estados:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion   = e['DESCRIPCION']
                for u in usuarios:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa       = p['NOMBREEMPRESA']
                        nombreCoachee       = u['NOMBRE']
                        apellidoCoachee     = u['APELLIDO']
                        correoCoachee       = u['CORREO']
                        telefonoCoachee     = u['FONO']
                        cantsesiones        = p['CANTSESIONES']
                        fechaIni            = p["FECHACREACION"]
                        objetivo            = p['OBJETIVOS']
                        indicadores         = p['INDICADORES']
                        planAccion          = p['PLANACCION']
                        nombreJefe          = u['NOMBREJEFE']
                        emailJefe           = u['EMAILJEFE']
                        fonoJefe            = u['FONOJEFE']
                        idProceso           = p['ID']
                        #se almacenan los datos en una variable
                        datos = [{
                            "NOMBREEMPRESA" : nombreEmpresa,
                            "NOMBRE"        : nombreCoachee,
                            "APELLIDO"      : apellidoCoachee,
                            "CORREO"        : correoCoachee,
                            "FONO"          : telefonoCoachee,
                            "CANTSESIONES"  : cantsesiones,
                            "OBJETIVOS"     : objetivo,
                            "FECHACREACION" : fechaIni,
                            "INDICADORES"   : indicadores,
                            "PLANACCION"    : planAccion,
                            "NOMBREJEFE"    : nombreJefe,
                            "EMAILJEFE"     : emailJefe,
                            "FONOJEFE"      : fonoJefe,
                            "DESCRIPCION"   : estadoDescripcion,
                            "ID"            : idProceso
                        }]
                        #se almacena una array de objetos
                        listados = datos + listados
                        #se ordena el listado almacenado
                        listadoProcesosOrdenados = sorted(listados, key=lambda k: k['ID'], reverse=True)
            
            #consulta de sesiones agendadas por proceso y usuarios para el calendario
            contador = 1 
            for pCal in procesosCal:
                querySesionesCal    = 'ordering=ID&PROCESO_ID='+str(pCal['ID'])
                sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
                for sCal in sesionesCalendario:
                    for u in usuarios:
                        #consulta por el usuario
                        if pCal['COACHEE_ID'] == u['ID']:
                            #consulta por la id del proceso para traer las sesiones correspondientes
                            if pCal['ID'] == sCal['PROCESO_ID']:
                                fechaSesion     = sCal['FECHASESION']
                                estadoSesion    = sCal['ESTADOSESION_ID']
                                nombreEmpresa   = pCal['NOMBREEMPRESA']
                                nombreCoachee   = u['NOMBRE']
                                apellidoCoachee = u['APELLIDO']
                                #se almacenan los datos en una variable
                                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                                    sesionCalendario = [{
                                        "NOMBREEMPRESA"     : nombreEmpresa,
                                        "NOMBRE"            : nombreCoachee,
                                        "APELLIDO"          : apellidoCoachee,
                                        "FECHASESION"       : fechaSesion,
                                        "ESTADOSESION_ID"   :estadoSesion,
                                        "CONTADOR"          : contador
                                    }]
                                    #se almacena una array de objetos 
                                    listadoSesionesCalendario = sesionCalendario + listadoSesionesCalendario 
                                    contador += 1
                                else:
                                    contador += 1
                                #Se restablece contador en base a la cantidad de sesiones por proceso.
                                if contador > pCal['CANTSESIONES']:
                                    contador = 1
            
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listadoProcesosOrdenados,
                'sesiones': listadoSesionesCalendario
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
    try:
        #se obtine json con token y datos del perfil del usuario
        perfil  = perfilUsuario(request)
        if perfil['perfil'] == 2:
            #se almacena id del usuario para usarlo de filtro para los procesos
            id  = perfil['id']
            #se obtiene el dia actual para usarlo como filtro para la fecha de sesiones
            day = datetime.today().strftime('%Y-%m-%d')
            #variable que almacena la url de la api
            querysesionesDelDia = 'ordering=-ID&FECHASESION=' + str(day)
            queryprocesoDelDia  = 'ordering=-ID&COACH_ID=' + str(id)
            querySesionesCal    = 'ordering=-ID'
            queryProcesosCal    = 'ACTIVO=1'
            #obtiene los datos desde la api enviando token de seguridad
            sesionesDelDia      = SesionesAPICall.get(request, querysesionesDelDia)
            procesosDelDia      = ProcesosAPICall.get(request,queryprocesoDelDia)
            usuarios            = UsuariosAPICall.get(request, None)
            estadoDelDia        = EstadosSesionesAPICall.get(request, None)
            estadoProc          = EstadosProcesosAPICall.get(request, None)
            sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
            procesosCal         = ProcesosAPICall.get(request,queryProcesosCal)
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            listaSesionesCalendario = []
            #consulta de sesiones por proceso, estado y usuarios
            for p in procesosDelDia:
                for s in sesionesDelDia:
                    if p['ID'] == s['PROCESO_ID']:
                        if s['FECHASESION'] is not None:
                            for ep in estadoProc:
                                if ep['ID'] == p['ESTADOPROCESO_ID']:
                                    estadoProceso   = ep['DESCRIPCION']
                                    estadoProce     = p['ESTADOPROCESO_ID']
                            for e in estadoDelDia:
                                if s['ESTADOSESION_ID'] == e['ID']:
                                    estadoDescripcion = e['DESCRIPCION']
                            for u in usuarios:
                                if p['COACHEE_ID'] == u['ID']:
                                    nombreEmpresa   = p['NOMBREEMPRESA']
                                    nombreCoachee   = u['NOMBRE']
                                    apellidoCoachee = u['APELLIDO']
                                    idProceso       = p['ID']
                            for uc in usuarios:
                                if p['COACH_ID'] == uc['ID']:
                                    nombreCoach     = uc['NOMBRE']
                                    apellidoCoach   = uc['APELLIDO']
                                    #se almacenan los datos en una variable
                                    json = [{
                                        "NOMBREEMPRESA"     : nombreEmpresa,
                                        "NOMBRE"            : nombreCoachee,
                                        "APELLIDO"          : apellidoCoachee,
                                        "DESCRIPCION"       : estadoDescripcion,
                                        "NOMBRECOACH"       : nombreCoach,
                                        "APELLIDOCOACH"     : apellidoCoach,
                                        "ID"                : idProceso,
                                        "ESTADOPROC"        : estadoProce,
                                        "DESCRIPCIONPROCE"  : estadoProceso
                                    }]
                                    #se almacena una array de objetos
                                    listados = json + listados                 
                        break
            #consulta de sesiones agendadas por proceso y usuarios para el calendario
            contadorCal = 1 
            for pCal in procesosCal:
                querySesionesCal    = 'ordering=ID&PROCESO_ID='+str(pCal['ID'])
                sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
                for sCal in sesionesCalendario:
                    #Descarta las sesiones Finalizadas y sin fecha 
                    for u in usuarios:
                        #consulta por el usuario
                        if pCal['COACHEE_ID'] == u['ID']:
                            #consulta por la id del proceso para traer las sesiones correspondientes
                            if pCal['ID'] == sCal['PROCESO_ID']:
                                fechaSesion     = sCal['FECHASESION']
                                estadoSesion    = sCal['ESTADOSESION_ID']
                                nombreEmpresa   = pCal['NOMBREEMPRESA']
                                nombreCoachee   = u['NOMBRE']
                                apellidoCoachee = u['APELLIDO']
                                #se filtran sesiones con estado finalizado y sin fecha
                                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                                #se almacenan los datos en una variable
                                    sesionCalendario = [{
                                        "NOMBREEMPRESA"     : nombreEmpresa,
                                        "NOMBRE"            : nombreCoachee,
                                        "APELLIDO"          : apellidoCoachee,
                                        "FECHASESION"       : fechaSesion,
                                        "ESTADOSESION_ID"   : estadoSesion,
                                        "CONTADOR"          : contadorCal
                                    }]
                                    #se almacena una array de objetos
                                    listaSesionesCalendario = sesionCalendario + listaSesionesCalendario
                                    contadorCal += 1
                                else:
                                    contadorCal += 1
                                #Se restablece contador en base a la cantidad de sesiones por proceso.
                                if contadorCal > pCal['CANTSESIONES']:
                                    contadorCal = 1

            #consulta de sesiones por proceso
            listadoBar = []
            listadoBarOrdenado = []
            contador = 1
            for sePro in procesosDelDia:
                querySesion         = 'ordering=ID&PROCESO_ID='+str(sePro['ID'])
                listadoSesiones     = SesionesAPICall.get(request,querySesion)
                for s in listadoSesiones:
                    datoSesionesBar = [{
                            "IDP"               :sePro['ID'],
                            "IDS"               :s['ID'],
                            "ESTADOSESION_ID"   :s['ESTADOSESION_ID'],
                            "COUNT"             : contador
                        }]
                    contador += 1

                    listadoBar = datoSesionesBar + listadoBar
                    listadoBarOrdenado = sorted(listadoBar, key = lambda k : k['IDS'])
                    if contador > sePro['CANTSESIONES']:
                        contador = 1

            #se obtiene la primera pagina del paginador
            page = request.GET.get('page', 1)

            try:
                #se le dan los atributos al paginador, listado de 4 por pagina
                paginator   = Paginator(listados, 3)
                #se almacenan los resultados por por pagina
                listado     = paginator.page(page)
            #si ocurre un error mostrara pagina no encontrada.
            except:
                raise Http404
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario'   : perfil,
                'entity'    : listado,
                'paginator' : paginator,
                'sesiones'  : listaSesionesCalendario,
                'sesionBar' : listadoBarOrdenado
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
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')

#--------------------------------------------menu coachee--------------------------------------------
def menuCoachee(request):
    try:
        #se obtine json con token y datos del perfil del usuario
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al de coachee
        if perfil['perfil'] == 3:
            #se almacena id del usuario para usarlo de filtro para los procesos
            id = perfil['id']
            #variable que almacena la url de la api
            procesoDelCoachee   = 'ordering=-ID&COACHEE_ID=' + str(id)
            queryProcesosCal    = 'ACTIVO=1'
            #obtiene los datos desde la api enviando token de seguridad
            proceso     = ProcesosAPICall.get(request,procesoDelCoachee)
            usuario     = UsuariosAPICall.get(request, None)
            procesosCal = ProcesosAPICall.get(request,queryProcesosCal)
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            listadoDatosBar = []
            listadoBarOrdenado = []
            #variable que almacenara los datos de sesiones que se utilizaran para lista de sesiones
            listaSesionesCalendario = []
            #fijamos cantidad de sesiones como 0
            canSesiones = 0
            #consulta de procesos por usuarios
            for p in proceso:
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa   = p['NOMBREEMPRESA']
                        nombreCoachee   = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        idProceso       = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach     = uc['NOMBRE']
                        apellidoCoach   = uc['APELLIDO']
                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA" : nombreEmpresa,
                            "NOMBRE"        : nombreCoachee,
                            "APELLIDO"      : apellidoCoachee,
                            "NOMBRECOACH"   : nombreCoach,
                            "APELLIDOCOACH" : apellidoCoach,
                            "IDSESION"      : canSesiones,
                            "ID"            : idProceso
                        }]
                        #se almacena una array de objetos
                        listados = json + listados
            #consulta de sesiones por proceso
            contador = 1
            for sePro in proceso:
                querySesion         = 'ordering=ID&PROCESO_ID='+str(sePro['ID'])
                listadoSesiones     = SesionesAPICall.get(request,querySesion)
                for s in listadoSesiones:
                    datoSesionesBar = [{
                            "IDP"               :sePro['ID'],
                            "IDS"               :s['ID'],
                            "ESTADOSESION_ID"   :s['ESTADOSESION_ID'],
                            "COUNT"             :contador
                        }]
                    contador += 1

                    listadoDatosBar = datoSesionesBar + listadoDatosBar
                    listadoBarOrdenado = sorted(listadoDatosBar, key = lambda k : k['IDS'])
                    if contador > sePro['CANTSESIONES']:
                        contador = 1

            #consulta de sesiones agendadas por proceso y usuarios para el calendario
            contadorCal = 1 
            for pCal in procesosCal:
                querySesionesCal    = 'ordering=ID&PROCESO_ID='+str(pCal['ID'])
                sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
                for sCal in sesionesCalendario:
                    #consulta por el usuario
                    if pCal['COACHEE_ID'] == id:
                        #consulta por la id del proceso para traer las sesiones correspondientes
                        if pCal['ID'] == sCal['PROCESO_ID']:
                            fechaSesion     = sCal['FECHASESION']
                            estadoSesion    = sCal['ESTADOSESION_ID']
                            nombreEmpresa   = pCal['NOMBREEMPRESA']
                            nombreCoachee   = perfil['nombreUsuario']
                            apellidoCoachee = perfil['apellidoUsuario']
                            #se filtran sesiones con estado finalizado y sin fecha
                            if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                            #se almacenan los datos en una variable
                                sesionCalendario = [{
                                    "NOMBREEMPRESA"     : nombreEmpresa,
                                    "NOMBRE"            : nombreCoachee,
                                    "APELLIDO"          : apellidoCoachee,
                                    "FECHASESION"       : fechaSesion,
                                    "ESTADOSESION_ID"   : estadoSesion,
                                    "CONTADOR"          : contadorCal
                                }]
                                #se almacena una array de objetos
                                listaSesionesCalendario = sesionCalendario + listaSesionesCalendario
                                contadorCal += 1
                            else:
                                contadorCal += 1
                            #Se restablece contador en base a la cantidad de sesiones por proceso.
                            if contadorCal > pCal['CANTSESIONES']:
                                contadorCal = 1
            #se obtiene la primera pagina del paginador
            page = request.GET.get('page', 1)

            try:
                #se le dan los atributos al paginador, listado de 4 por pagina
                paginator   = Paginator(listados, 4)
                #se almacenan los resultados por por pagina
                listado     = paginator.page(page)
            #si ocurre un error mostrara pagina no encontrada.
            except:
                raise Http404
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario'   : perfil,
                'entity'    : listado,
                'paginator' : paginator,
                'sesiones'  : listaSesionesCalendario,
                'listaBar'  : listadoBarOrdenado
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            queryProcesos       = 'ordering=-ID&limit=5'
            queryprocesosCal    = 'ESTADOPROCESO_ID!=4'
            querySesionesCal    = 'ordering=-ID'
            #obtiene los datos desde la api enviando token de seguridad
            proceso             = ProcesosAPICall.get(request, queryProcesos)
            usuario             = UsuariosAPICall.get(request, None)
            estado              = EstadosProcesosAPICall.get(request, None)
            sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
            procesosCal         = ProcesosAPICall.get(request, queryprocesosCal)
            #variable que almacenara el listado de procesos y sus datos
            listados = []
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            listadoSesionesCalendario = []
            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa   = p['NOMBREEMPRESA']
                        nombreCoachee   = u['NOMBRE']
                        apellidoCoachee = u['APELLIDO']
                        correoCoachee   = u['CORREO']
                        telefonoCoachee = u['FONO']
                        cantsesiones    = p['CANTSESIONES']
                        fechaIni        = p["FECHACREACION"]
                        objetivo        = p['OBJETIVOS']
                        indicadores     = p['INDICADORES']
                        planAccion      = p['PLANACCION']
                        nombreJefe      = u['NOMBREJEFE']
                        emailJefe       = u['EMAILJEFE']
                        fonoJefe        = u['FONOJEFE']
                        idProceso       = p['ID']
                        #se almacenan los datos en una variable
                        json = [{
                            "NOMBREEMPRESA" : nombreEmpresa,
                            "NOMBRE"        : nombreCoachee,
                            "APELLIDO"      : apellidoCoachee,
                            "CORREO"        : correoCoachee,
                            "FONO"          : telefonoCoachee,
                            "CANTSESIONES"  : cantsesiones,
                            "OBJETIVOS"     : objetivo,
                            "FECHACREACION" : fechaIni,
                            "INDICADORES"   : indicadores,
                            "PLANACCION"    : planAccion,
                            "NOMBREJEFE"    : nombreJefe,
                            "EMAILJEFE"     : emailJefe,
                            "FONOJEFE"      : fonoJefe,
                            "DESCRIPCION"   : estadoDescripcion,
                            "ID"            : idProceso
                        }]
                        #se almacena una array de objetos
                        listados = json + listados

            #consulta de sesiones agendadas por proceso y usuarios para el calendario
            contador = 1 
            for pCal in procesosCal:
                querySesionesCal    = 'ordering=ID&PROCESO_ID='+str(pCal['ID'])
                sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
                for sCal in sesionesCalendario:
                    for u in usuario:
                        #consulta por el usuario
                        if pCal['COACHEE_ID'] == u['ID']:
                            #consulta por la id del proceso para traer las sesiones correspondientes
                            if pCal['ID'] == sCal['PROCESO_ID']:
                                fechaSesion     = sCal['FECHASESION']
                                estadoSesion    = sCal['ESTADOSESION_ID']
                                nombreEmpresa   = pCal['NOMBREEMPRESA']
                                nombreCoachee   = u['NOMBRE']
                                apellidoCoachee = u['APELLIDO']
                                #se almacenan los datos en una variable
                                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                                    sesionCalendario = [{
                                        "NOMBREEMPRESA"     : nombreEmpresa,
                                        "NOMBRE"            : nombreCoachee,
                                        "APELLIDO"          : apellidoCoachee,
                                        "FECHASESION"       : fechaSesion,
                                        "ESTADOSESION_ID"   :estadoSesion,
                                        "CONTADOR"          : contador
                                    }]
                                    #se almacena una array de objetos 
                                    listadoSesionesCalendario = sesionCalendario + listadoSesionesCalendario 
                                    contador += 1
                                else:
                                    contador += 1
                                #Se restablece contador en base a la cantidad de sesiones por proceso.
                                if contador > pCal['CANTSESIONES']:
                                    contador = 1
                                    
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario'   : perfil,
                'entity'    : listados,
                'sesiones'  : listadoSesionesCalendario
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            procesoCal          = 'ESTADOPROCESO_ID!=4'
            querySesionesCal    = 'ordering=-ID'
            #obtiene los datos desde la api enviando token de seguridad
            usuario             = UsuariosAPICall.get(request,None)
            sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
            procesosCal         = ProcesosAPICall.get(request, procesoCal)
            #variable que almacenara los datos de sesiones que se utilizaran para el calendario
            listadoSesionesCalendario = []
            #consulta por el tipo de metodo y si el perfil corresponde al del administrador
            if request.method == 'POST' and perfil['perfil'] == 1:
                # Obtener datos del Front
                NOMBREEMPRESA   = request.POST.get('nombreEmpre')
                CANTSESIONES    = request.POST.get('cantiSesiones')
                OBJETIVOS       = None
                INDICADORES     = None
                PLANACCION      = None
                COACH_ID        = request.POST.get('coachProces')
                COACHEE_ID      = request.POST.get('coacheeProces')

                # Creo Json para enviar los datos a la api
                json = {
                    "NOMBREEMPRESA" : NOMBREEMPRESA.title(),
                    "CANTSESIONES"  : CANTSESIONES,
                    "OBJETIVOS"     : OBJETIVOS,
                    "INDICADORES"   : INDICADORES,
                    "PLANACCION"    : PLANACCION,
                    "COACH_ID"      : COACH_ID,
                    "COACHEE_ID"    : COACHEE_ID
                }
                # Metodo para crear procesos en API
                response = ProcesosAPICall.post(request,json)
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

            #consulta de sesiones agendadas por proceso y usuarios para el calendario
            contador = 1 
            for pCal in procesosCal:
                querySesionesCal    = 'ordering=ID&PROCESO_ID='+str(pCal['ID'])
                sesionesCalendario  = SesionesAPICall.get(request,querySesionesCal)
                for sCal in sesionesCalendario:
                    for u in usuario:
                        #consulta por el usuario
                        if pCal['COACHEE_ID'] == u['ID']:
                            #consulta por la id del proceso para traer las sesiones correspondientes
                            if pCal['ID'] == sCal['PROCESO_ID']:
                                fechaSesion     = sCal['FECHASESION']
                                estadoSesion    = sCal['ESTADOSESION_ID']
                                nombreEmpresa   = pCal['NOMBREEMPRESA']
                                nombreCoachee   = u['NOMBRE']
                                apellidoCoachee = u['APELLIDO']
                                #se almacenan los datos en una variable
                                if sCal['ESTADOSESION_ID'] != 4 and sCal['FECHASESION'] is not None:
                                    sesionCalendario = [{
                                        "NOMBREEMPRESA"     : nombreEmpresa,
                                        "NOMBRE"            : nombreCoachee,
                                        "APELLIDO"          : apellidoCoachee,
                                        "FECHASESION"       : fechaSesion,
                                        "ESTADOSESION_ID"   :estadoSesion,
                                        "CONTADOR"          : contador
                                    }]
                                    #se almacena una array de objetos 
                                    listadoSesionesCalendario = sesionCalendario + listadoSesionesCalendario 
                                    contador += 1
                                else:
                                    contador += 1
                                #Se restablece contador en base a la cantidad de sesiones por proceso.
                                if contador > pCal['CANTSESIONES']:
                                    contador = 1

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario'       : perfil,
                'list_usuario'  : usuario,
                'sesiones'      : listadoSesionesCalendario
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            orderProcesos = 'ordering=-ID'
            #obtiene los datos desde la api enviando token de seguridad
            proceso = ProcesosAPICall.get(request,orderProcesos)
            usuario = UsuariosAPICall.get(request,None)
            estado  = EstadosProcesosAPICall.get(request, None)
            #variable que almacenara el listado de procesos y sus datos
            listadoDatos = []
            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        estadoDescripcion   = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa       = p['NOMBREEMPRESA']
                        nombreCoachee       = u['NOMBRE']
                        apellidoCoachee     = u['APELLIDO']
                        correoCoachee       = u['CORREO']
                        telefonoCoachee     = u['FONO']
                        fechaCreacion       = p['FECHACREACION']
                        cantsesiones        = p['CANTSESIONES']
                        objetivo            = p['OBJETIVOS']
                        indicadores         = p['INDICADORES']
                        planAccion          = p['PLANACCION']
                        nombreJefe          = u['NOMBREJEFE']
                        emailJefe           = u['EMAILJEFE']
                        fonoJefe            = u['FONOJEFE']
                        idProceso           = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach         = uc['NOMBRE']
                        apellidoCoach       = uc['APELLIDO']

                        #se almacenan los datos en una variable
                        datos = [{
                            "NOMBREEMPRESA" : nombreEmpresa,
                            "NOMBRE"        : nombreCoachee,
                            "APELLIDO"      : apellidoCoachee,
                            "CORREO"        : correoCoachee,
                            "FONO"          : telefonoCoachee,
                            "FECHACREACION" : fechaCreacion,
                            "CANTSESIONES"  : cantsesiones,
                            "OBJETIVOS"     : objetivo,
                            "INDICADORES"   : indicadores,
                            "PLANACCION"    : planAccion,
                            "NOMBREJEFE"    : nombreJefe,
                            "EMAILJEFE"     : emailJefe,
                            "FONOJEFE"      : fonoJefe,
                            "DESCRIPCION"   : estadoDescripcion,
                            "NOMBRECOACH"   : nombreCoach,
                            "APELLIDOCOACH" : apellidoCoach,
                            "ID"            : idProceso
                        }]

                        #se almacena una array de objetos
                        listadoDatos = datos + listadoDatos

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario'   : perfil,
                'entity'    : listadoDatos,
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #consulta por el tipo de metodo
            if request.method == 'POST':
                # Obtener datos del Front
                ID              = id
                NOMBREEMPRESA   = request.POST.get('nombreEmpresa')
                CANTSESIONES    = request.POST.get('cantidadSesiones')
                FECHACREACION   = request.POST.get('fechaCreacion')

                # Creo Json para enviar los datos a la api
                modificarProcesoJson = {
                    "ID"            : ID,
                    "NOMBREEMPRESA" : NOMBREEMPRESA.title(),
                    "CANTSESIONES"  : CANTSESIONES,
                    "FECHACREACION" : FECHACREACION
                }

                # Metodo para modificar procesos en API
                response = ProcesosAPICall.put(request, modificarProcesoJson,id)
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            queryProcesos   = 'ordering=-ID&ID=' + str(id)
            querySesiones   = 'ordering=ID&PROCESO_ID='+str(id)
            #obtiene los datos desde la api enviando token de seguridad
            proceso         = ProcesosAPICall.get(request, queryProcesos)
            usuario         = UsuariosAPICall.get(request, None)
            estado          = EstadosProcesosAPICall.get(request,None)
            sesiones        = SesionesAPICall.get(request, querySesiones)
            estadoSesion    = EstadosSesionesAPICall.get(request, None)
            gestorArchivo   = ArchivosAPICall.get(request,None)
            enlace          = EnlacesAPICall.get(request, None)
            
            #variable que almacenara el listado de procesos y sus datos
            listadoDatos = []
            listadoGestor = []
            listadoEnlaces = []
            #consulta de procesos por estadoproceso y usuarios
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID'] == e['ID']:
                        idProcesoEstado     = p['ESTADOPROCESO_ID']
                        estadoDescripcion   = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID'] == u['ID']:
                        nombreEmpresa       = p['NOMBREEMPRESA']
                        nombreCoachee       = u['NOMBRE']
                        apellidoCoachee     = u['APELLIDO']
                        correoCoachee       = u['CORREO']
                        telefonoCoachee     = u['FONO']
                        fechaCreacion       = p['FECHACREACION']
                        cantsesiones        = p['CANTSESIONES']
                        objetivo            = p['OBJETIVOS']
                        indicadores         = p['INDICADORES']
                        planAccion          = p['PLANACCION']
                        nombreJefe          = u['NOMBREJEFE']
                        emailJefe           = u['EMAILJEFE']
                        fonoJefe            = u['FONOJEFE']
                        idProceso           = p['ID']
                for uc in usuario:
                    if p['COACH_ID'] == uc['ID']:
                        nombreCoach         = uc['NOMBRE']
                        apellidoCoach       = uc['APELLIDO']

                        #se almacenan los datos en una variable
                        datos = [{
                            "NOMBREEMPRESA"     : nombreEmpresa,
                            "NOMBRE"            : nombreCoachee,
                            "APELLIDO"          : apellidoCoachee,
                            "CORREO"            : correoCoachee,
                            "FONO"              : telefonoCoachee,
                            "FECHACREACION"     : fechaCreacion,
                            "CANTSESIONES"      : cantsesiones,
                            "OBJETIVOS"         : objetivo,
                            "INDICADORES"       : indicadores,
                            "PLANACCION"        : planAccion,
                            "NOMBREJEFE"        : nombreJefe,
                            "EMAILJEFE"         : emailJefe,
                            "FONOJEFE"          : fonoJefe,
                            "DESCRIPCION"       : estadoDescripcion,
                            "NOMBRECOACH"       : nombreCoach,
                            "APELLIDOCOACH"     : apellidoCoach,
                            "ID"                : idProceso,
                            "IDESTADOPROCESO"   : idProcesoEstado
                        }]

                        #se almacena una array de objetos
                        listadoDatos = datos + listadoDatos
            #consulta para obtener la id de los archivos y links asociados a la sesion
            # to do
                for s in sesiones:
                    for g in gestorArchivo:
                        if s['ID'] == g['SESION_ID']:
                            nombre = g['LINK'].replace("https://res.cloudinary.com/duocuc/raw/upload/v1/upload/",'')
                            idLinkGestor    = g['SESION_ID']
                            linkGestor      = g['LINK']
                            datosGestor = [{
                                "IDLINKGE"  : idLinkGestor,
                                "LINKGE"    : linkGestor,
                                "NOMBREARCHIVO": nombre,
                            }]

                            listadoGestor = datosGestor + listadoGestor
                for s in sesiones:
                    for en in enlace:
                        if s['ID'] == en['SESION_ID']:
                            idlinkEnlace    = en['SESION_ID']
                            linkEnlace      = en['LINK']   
                            datosEnlaces = [{
                                "IDLINKEN"  : idlinkEnlace,
                                "LINKEN"    : linkEnlace
                            }]

                            #se almacena una array de objetos
                            listadoEnlaces = datosEnlaces + listadoEnlaces

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario'       : perfil,
                'entity'        : listadoDatos,
                'sesiones'      : sesiones,
                'estadosSesion' : estadoSesion,
                'gestores'      : listadoGestor,
                'enlaces'       : listadoEnlaces
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
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
            response = ProcesosAPICall.put(request,finProcesoJson,id)
           
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #variable que almacena la url de la api
            usuariosCoach   = 'ordering=-ID&limit=5&PERFIL_ID=2'
            usuariosCoachee = 'ordering=-ID&limit=5&PERFIL_ID=3'
            #obtiene los datos desde la api enviando token de seguridad
            listadoCoachs = UsuariosAPICall.get(request, usuariosCoach)
            listadoCoachees = UsuariosAPICall.get(request, usuariosCoachee)

            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'list_coachs': listadoCoachs,
                'list_coachees': listadoCoachees
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
        perfil = perfilUsuario(request)
        data = {'usuario': perfil}
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            # Crear usuario
            if request.method == 'POST':
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
                response = UsuariosAPICall.post(request, crearUsuariosJson)

                #se almacenan las variables con los datos en un objeto para enviarlo a la vista
                
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al administrador
        if perfil['perfil'] == 1:
            #obtiene los datos desde la api enviando token de seguridad
            usuarios = UsuariosAPICall.get(request,None)
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
        perfil = perfilUsuario(request)
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
                response = UsuariosAPICall.put(request, modificaUsuarioJson, id)        
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al coach
        if perfil['perfil'] == 2:
            #variable que almacena la url de la api
            order = 'ordering=-ID&COACH_ID=' + str(perfil['id'])            
            #obtiene los datos desde la api enviando token de seguridad
            proceso = ProcesosAPICall.get(request, order)
            usuario = UsuariosAPICall.get(request,None)
            estado = EstadosProcesosAPICall.get(request, None)
            #variable que almacenara el listado de procesos y sus datos
            listadoDatos = []
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
                        datos = [{
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
                        listadoDatos = datos + listadoDatos
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listadoDatos,
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
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al coach
        if perfil['perfil'] == 2:
            #variable que almacena la url de la api
            queryProcesos = '?ordering=-ID&ESTADOPROCESO_ID=1&COACH_ID=' + str(perfil['id'])
            #obtiene los datos desde la api enviando token de seguridad
            proceso = ProcesosAPICall.get(request, queryProcesos)
            usuario = UsuariosAPICall.get(request, None)
            estado = EstadosProcesosAPICall.get(request, None)
            #variable que almacenara el listado de procesos y sus datos
            listadoDatos = []
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
                        datos = [{
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
                        listadoDatos = datos + listadoDatos
            #se obtiene la primera pagina del paginador
            page = request.GET.get('page', 1)
            try:
                #se le dan los atributos al paginador, listado de 10 por pagina
                paginator = Paginator(listadoDatos, 10)
                #se almacenan los resultados por por pagina
                listadoDatosOrdenado = paginator.page(page)
            #si ocurre un error mostrara pagina no encontrada.
            except:
                raise Http404
            #se almacenan las variables con los datos en un objeto para enviarlo a la vista
            data = {
                'usuario': perfil,
                'entity': listadoDatosOrdenado,
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
        perfil = perfilUsuario(request)
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
                response = ProcesosAPICall.put(request, modProcCoach, id)
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
                queryProcesos = 'ordering=-ID&ID=' + str(id)
                querySesiones = 'ordering=ID&PROCESO_ID='+str(id)
                #obtiene los datos desde la api enviando token de seguridad
                proceso = ProcesosAPICall.get(request,queryProcesos)
                usuario = UsuariosAPICall.get(request, None)
                estado = EstadosProcesosAPICall.get(request, None)
                sesiones = SesionesAPICall.get(request, querySesiones)
                estadoSesion = EstadosSesionesAPICall.get(request, None)
                gestorArchivo = ArchivosAPICall.get(request,None)
                enlace = EnlacesAPICall.get(request, None)
                #variable que almacenara el listado de procesos y sus datos
                listadoDatos = []
                #variable que almacenara el listado de archivos
                listadoGestorArchivo = []
                listadoGestorEnlace = []

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
                            datos = [{
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
                            listadoDatos = datos + listadoDatos

                #consulta para obtener la id de los archivos y links asociados a la sesion
                for s in sesiones:
                    for g in gestorArchivo:
                        if s['ID'] == g['SESION_ID']:
                            nombre = g['LINK'].replace("https://res.cloudinary.com/duocuc/raw/upload/v1/upload/",'')
                            linkGestor = g['LINK']
                            datosLG = [{
                                    "ID": g['ID'],
                                    "IDLINKGE": g['SESION_ID'],
                                    "LINKGE": linkGestor,
                                    "NOMBREARCHIVO": nombre
                                }]
                            
                            listadoGestorArchivo = datosLG + listadoGestorArchivo
                
                for s in sesiones:
                    for en in enlace:
                        if s['ID'] == en['SESION_ID']:
                            linkEnlace = en['LINK']  
                            datosLE = [{
                                    "ID": en['ID'],
                                    "IDLINKEN": en['SESION_ID'],
                                    "LINKEN": linkEnlace
                                }]
                            #se almacena una array de objetos
                            listadoGestorEnlace = datosLE + listadoGestorEnlace
                
                #se almacenan las variables con los datos en un objeto para enviarlo a la vista
                data = {
                    'usuario': perfil,
                    'entity': listadoDatos,
                    'sesiones': sesiones,
                    'estados': estado,
                    'estadosSesion': estadoSesion,
                    'gestoresEnlaces': listadoGestorEnlace,
                    'gestoresArchivos': listadoGestorArchivo
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
    # except Exception as e:
    #     messages.warning(request,'Ingrese sus credenciales para acceder')
    #     return redirect('/')

# ----------------------------------Modificar sesiones Coach----------------------------------
def infoEnlaceSesionCoach(request,id):
    perfil = perfilUsuario(request)

    if perfil['perfil'] == 2:
            #se obtiene dato desde la vista
            idP = request.POST.get('proceso')
            if request.method == 'POST':
                link = request.POST.get('link')

                gestorEnlace = {
                    "LINK": link,
                    "SESION_ID": id,
                }

                #metodo para modificar sesion
                responseEnlaces = EnlacesAPICall.post(request,gestorEnlace)

                if responseEnlaces.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Enlace añadido.')
                    return redirect('infoProCoach', idP)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    # se reemplazan comillas dobles que trae el mensaje desde la api
                    responseEnlaces.encoding = 'utf-8'
                    messages.error(
                        request, responseEnlaces.text.replace('"', ''))
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

def infoArchivoSesionCoach(request,id):
    perfil = perfilUsuario(request)

    if perfil['perfil'] == 2:
            #se obtiene dato desde la vista
            idP = request.POST.get('proceso')
            if request.method == 'POST':
                archivo = request.FILES.get('archivo')
                name=str(archivo.name)
                archivo1 = archivo.open(name)
                
                archivoEncoded = base64.b64encode(archivo1.read()).decode('utf-8')
                archivoEncoded1 = str(archivoEncoded)
                gestorArchivo = {
                                    "file_name" : str(request.FILES['archivo']),
                                    "content": str(request.FILES['archivo'].content_type),
                                    "tell" : str(request.FILES['archivo'].tell()),
                                    "LINK": archivoEncoded1,
                                    "SESION_ID": id,
                                    "TIPOARCHIVO_ID": 1
                                }
                

                #metodo para modificar sesion

                responseArchivo = ArchivosAPICall.post(request,gestorArchivo)

                if responseArchivo.status_code == 201:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Archivo añadido.')
                    return redirect('infoProCoach', idP)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    # se reemplazan comillas dobles que trae el mensaje desde la api
                    responseArchivo.encoding = 'utf-8'
                    messages.error(
                        request, responseArchivo.text.replace('"', ''))
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

def infoEnlaceEliminar(request, id):
    perfil = perfilUsuario(request)

    if perfil['perfil'] == 2:
            #se obtiene dato desde la vista
            idP = request.POST.get('proceso')
            sesid = request.POST.get('sesion')
            if request.method == 'POST':

                #metodo para modificar sesion
                responseEnlaces = EnlacesAPICall.delete(request,sesid,id)

                if responseEnlaces.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Enlace Eliminado.')
                    return redirect('infoProCoach', idP)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    # se reemplazan comillas dobles que trae el mensaje desde la api
                    responseEnlaces.encoding = 'utf-8'
                    messages.error(
                        request, responseEnlaces.text.replace('"', ''))
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

def infoArchivoEliminar(request,id):
    perfil = perfilUsuario(request)

    if perfil['perfil'] == 2:
            #se obtiene dato desde la vista
            idP = request.POST.get('proceso')
            superid = request.POST.get('sesion')
            if request.method == 'POST':

                #metodo para modificar sesion
                responseArchivo = ArchivosAPICall.delete(request,superid,id)

                if responseArchivo.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Archivo Eliminado.')
                    return redirect('infoProCoach', idP)
                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    # se reemplazan comillas dobles que trae el mensaje desde la api
                    responseArchivo.encoding = 'utf-8'
                    messages.error(
                        request, responseArchivo.text.replace('"', ''))
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

def infoSesionCoach(request, id):
    #try:
        #se obtine json con token y datos del perfil del usuario
        perfil = perfilUsuario(request)
        
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

                #metodo para modificar sesion
                response = SesionesAPICall.put(request,modificarSesionesJson,id)
                
                #consulta respuesta de la api
                if response.status_code == 200:
                    #mensaje que muestra la vista si la actualización es exitosa
                    messages.success(request, 'Sesión actualizada con éxito.')
                    return redirect('infoProCoach', idP)

                #mensaje que muestra la vista si la actualización sufre algun problema
                else:
                    # se reemplazan comillas dobles que trae el mensaje desde la api
                    response.encoding = 'utf-8'
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
    #except Exception as e:
     #   messages.warning(request,'Ingrese sus credenciales para acceder')
      #  return redirect('/')


# ------------------------------  Perteneciente al Coachee ----------------------------------------------#

# ----------------------------------Procesos asignados al Coachee----------------------------------
def infoProCoachee(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        perfil = perfilUsuario(request)
        #se consulta si el perfil de usuario corresponde al coachee
        if perfil['perfil'] == 3:
            #consulta metodo a utilizar
            if request.method == 'GET':
                #variable que almacena la url de la api
                queryProcesos = 'ordering=-ID&ID=' + str(id)
                querySesiones = 'ordering=ID&PROCESO_ID='+str(id)
                #obtiene los datos desde la api enviando token de seguridad
                proceso         = ProcesosAPICall.get(request,queryProcesos)
                usuario         = UsuariosAPICall.get(request, None)
                estado          = EstadosProcesosAPICall.get(request, None)
                sesiones        = SesionesAPICall.get(request, querySesiones)
                estadoSesion    = EstadosSesionesAPICall.get(request, None)
                gestorArchivo   = ArchivosAPICall.get(request, None)
                enlace          = EnlacesAPICall.get(request,None)
                #variable que almacenara el listado de procesos y sus datos
                listadoDatos    = []
                #variable que almacenara los archivos de las sesiones
                listadoGestor   = []
                listadoEnlaces  = []
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
                            datos = [{
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
                            listadoDatos = datos + listadoDatos
                #consulta para obtener la id de los archivos y links asociados a la sesion
                for s in sesiones:
                    for g in gestorArchivo:
                        if s['ID'] == g['SESION_ID']:
                            nombre = g['LINK'].replace("https://res.cloudinary.com/duocuc/raw/upload/v1/upload/",'')
                            idLinkGestor = g['SESION_ID']
                            linkGestor = g['LINK']
                            datosGE = [{
                                        "IDLINKGE": idLinkGestor,
                                        "LINKGE": linkGestor,
                                        "NOMBREARCHIVO": nombre,
                                    }]
                            listadoGestor = datosGE + listadoGestor
                for s in sesiones:
                    for en in enlace:
                        if s['ID'] == en['SESION_ID']:
                            idlinkEnlace = en['SESION_ID']
                            linkEnlace = en['LINK']   
                            datosEN = [{
                                "IDLINKEN": idlinkEnlace,
                                "LINKEN": linkEnlace
                            }]
                            #se almacena una array de objetos
                            listadoEnlaces = datosEN + listadoEnlaces
                #se almacenan las variables con los datos en un objeto para enviarlo a la vista
                data = {
                    'usuario': perfil,
                    'entity': listadoDatos,
                    'sesiones': sesiones,
                    'estados': estado,
                    'estadosSesion': estadoSesion,
                    'gestores':listadoGestor,
                    'enlaces':listadoEnlaces
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
        #variable que almacena la url de la api
        queryProcesos = 'ordering=-ID&ID=' + str(id)
        querySesiones = 'PROCESO_ID='+str(id)
        #obtiene los datos desde la api enviando token de seguridad
        proceso     = ProcesosAPICall.get(request, queryProcesos)
        usuario     = UsuariosAPICall.get(request, None)
        estado      = EstadosProcesosAPICall.get(request, None)
        sesiones    = SesionesAPICall.get(request, querySesiones)
        #variable que almacenara el listado de procesos y sus datos
        listadoDatos = []

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
                    datos = [{
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
                    listadoDatos = datos + listadoDatos

        #se obtine diseño de pdf
        template = get_template("base/reporte.html")
        #se almacena datos que iran al pdf
        context = {
            'entity': listadoDatos,
            'sesiones': sesiones
        }

        # se cargan datos dentro del diseño del pdf y se agregan los estilos a este
        html_template = template.render(context)
        css_url = os.path.join(BASE_DIR, 'frontProject/static/css/bootstrap.css')

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

    #si ingresa a la url de menuCoachee sin token de seguridad redirecciona al login
    except Exception as e:
        messages.warning(request, 'Ingrese sus credenciales para acceder')
        return redirect('/')


# ---------------------- modificar plan de accion coachee----------
def modPlanAccion(request, id):
    try:
        #se obtine json con token y datos del perfil del usuario
        perfil = perfilUsuario(request)
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
                response = ProcesosAPICall.put(request, modificarPlanJson,id) 
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
        perfil = perfilUsuario(request)
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
                response = SesionesAPICall.put(request,modificarRespAvancesJson,IDs)
                
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