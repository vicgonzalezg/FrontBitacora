from frontProject.models import Usuario
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
import requests
from . import services
# Create your views here.
from django.core import serializers
import json
import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from datetime import datetime
from django.template.loader import get_template
from weasyprint import HTML, CSS
from bitacoraProject import settings 
from bitacoraProject.wsgi import *
import base64

#definimos el login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')
        #print(username,password)
        #r=services.LoginServices().generate_request(username,password)
        r = requests.post('http://127.0.0.1:8001/login', data = {'USUARIO':username,'CONTRASENA':password})
        #print(r.content)

        if r.status_code == 200:
            result = json.loads(r.content) 
            #print(result)
            nombre_usuario=result['USUARIO']['NOMBRE']+' '+result['USUARIO']['APELLIDO']
            perfil_usuario=result['USUARIO']['PERFIL_ID']
            nombre=result['USUARIO']['NOMBRE']
            apellido=result['USUARIO']['APELLIDO']
            correo=result['USUARIO']['CORREO']
            fono_usuario=result['USUARIO']['FONO']
            id_usuario = result['USUARIO']['ID']
            datos_usuario= {'nombre': nombre_usuario,
                            'perfil':perfil_usuario,
                            'id':id_usuario,
                            'fono':fono_usuario,
                            'nombreUsuario':nombre,
                            'apellidoUsuario':apellido,
                            'correo':correo}
            token = result['TOKEN']
            #print(token)
            #print('Hola soy un token que retorna don ivan: '+ token)
            headers = {
                    'content-type': "application/json",
                    'authorization': "Bearer " + token
                }
            request.session['Headers'] = headers
            
            request.session['Perfil_Usuario'] = datos_usuario
            #print(datos_usuario)
            #print(str(request.session['Headers']))
            #print(str(request.session['Perfil_Usuario']))
            plantilla=''
            if perfil_usuario==1:
                plantilla='menuAdmin'
            elif perfil_usuario==2:
                plantilla='menuCoach'
            elif perfil_usuario==3:
                plantilla='menuCoachee'
            return redirect(plantilla)
        else:
            messages.error(request, 'Usuario y/o contraseña incorrectos.')
            return render(request, 'login/login.html')
    return render(request, 'login/login.html')

#Cierre de sesión
def logout(request):
    try:
        #print('hola vengo de logout')
        headers = {'':''}
        request.session['Headers'] = headers
        return redirect('/')
    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
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

#Perfil de usuarios
def perfil(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        url = 'http://127.0.0.1:8001/usuarios'
        usuario = requests.get(url).json()

        data = {
            'usuario': perfil,
            'entity':usuario,
        }
        return render(request,'Perfil/perfil.html',data)
    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')        

#Paginas de Menu por Peril
def menuAdmin(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            #print(day)
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&limit=5'
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstado,headers=headers).json()
            listados = []
            #listado = proceso.update(usuario)
            if len(proceso) > 0:
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID']==e['ID']:
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID']==u['ID']:
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

                            json=[{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE":nombreCoachee,
                                "APELLIDO":apellidoCoachee,
                                "CORREO":correoCoachee,
                                "FONO":telefonoCoachee,
                                "CANTSESIONES":cantsesiones,
                                "OBJETIVOS": objetivo,
                                "FECHACREACION": fechaIni,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,  
                                "DESCRIPCION":estadoDescripcion
                                }]

                            listados = json + listados

                    data = {
                    'usuario': perfil,
                    'entity':listados,
                    }
            else:
                data = {
                    'usuario': perfil,
                    'entity':{'NOMBREEMPRESA':None},
                }
            print(data['entity'])
            return render(request,'menu/menuAdmin.html',data) 
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

def menuCoach(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 2:
            id=perfil['id']
            day = datetime.today().strftime('%Y-%m-%d')
            #print(day)
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&limit=5&FECHACREACION='+str(day)+'&COACH_ID='+str(id)
            urlSesionesCal = 'http://127.0.0.1:8001/procesos?ordering=-ID&COACH_ID='+str(id)
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            proceso = requests.get(urlProcesos,headers=headers).json()
            procesosCal = requests.get(urlSesionesCal,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstado,headers=headers).json()
            listados = []
            
            #listado = proceso.update(usuario)
            if len(proceso) > 0:
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID']==e['ID']:
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID']==u['ID']:
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
                        if p['COACH_ID'] ==uc['ID']:
                            nombreCoach= uc['NOMBRE']
                            apellidoCoach= uc['APELLIDO']

                            json=[{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE":nombreCoachee,
                                "APELLIDO":apellidoCoachee,
                                "CORREO":correoCoachee,
                                "FONO":telefonoCoachee,
                                "FECHACREACION":fechaCreacion,
                                "CANTSESIONES":cantsesiones,
                                "OBJETIVOS": objetivo,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,  
                                "DESCRIPCION":estadoDescripcion,
                                "NOMBRECOACH":nombreCoach,
                                "APELLIDOCOACH":apellidoCoach,
                                "ID": idProceso
                                }]

                            listados = json + listados
                
                page = request.GET.get('page',1)

                try:
                    paginator = Paginator(listados,4)
                    listado = paginator.page(page)

                except:
                    raise Http404
                
                data = {
                    'usuario': perfil,
                    'entity':listado,
                    'paginator':paginator,
                    'procesosCalendario':procesosCal
                }
                print(data)
            else:
                data = {
                'usuario': perfil,
                'entity':{'NOMBREEMPRESA':None},
                'procesosCalendario':procesosCal
                }
            print(data)
            return render(request,'menu/menuCoach.html', data)
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

def menuCoachee(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 3:
            id=perfil['id']
            #print(day)
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&COACHEE_ID='+str(id)
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            urlsesion = 'http://127.0.0.1:8001/sesiones'
            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstado,headers=headers).json()
            sesiones = requests.get(urlsesion,headers=headers).json()
            listados = []
            canSesiones = 0

            #listado = proceso.update(usuario)
            if len(proceso) > 0:
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID']==e['ID']:
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID']==u['ID']:
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
                        if p['COACH_ID'] ==uc['ID']:
                            nombreCoach= uc['NOMBRE']
                            apellidoCoach= uc['APELLIDO']
                    for s in sesiones:
                        if p['ID'] == s['PROCESO_ID']:
                            

                            json=[{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE":nombreCoachee,
                                "APELLIDO":apellidoCoachee,
                                "CORREO":correoCoachee,
                                "FONO":telefonoCoachee,
                                "FECHACREACION":fechaCreacion,
                                "CANTSESIONES":cantsesiones,
                                "OBJETIVOS": objetivo,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,  
                                "DESCRIPCION":estadoDescripcion,
                                "NOMBRECOACH":nombreCoach,
                                "APELLIDOCOACH":apellidoCoach,
                                "IDSESION": canSesiones,
                                "ID": idProceso
                                
                                }]

                            listados = json + listados

                page = request.GET.get('page',1)

                try:
                    paginator = Paginator(listados,4)
                    listado = paginator.page(page)

                except:
                    raise Http404
                print(listados)
                data = {
                    'usuario': perfil,
                    'entity':listado,
                    'paginator':paginator
                }
            else:
                data = {
                'usuario': perfil,
                'entity':{'NOMBREEMPRESA':None},
                }

            return render(request,'menu/menuCoachee.html', data)
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 2:
                plantilla='menuCoach'
            return redirect(plantilla)
    
    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

 #   except Exception as e:
 #       messages.warning(request,'Ingrese sus credenciales para acceder')
 #       return redirect('/')


###################Perteneciente al administrador-----------------------------------------------------

# --------------------------------  Paginas de Procesos ----------------------------------------------
#Procesos admin Principal
def procesosAdmin(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&limit=5'
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstados = 'http://127.0.0.1:8001/estados-procesos'

            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstados,headers=headers).json()
            listados = []
            if len(proceso) > 0:
                for p in proceso:
                    for e in estado:
                        #print(str(p['ESTADOPROCESO_ID']))
                        #print(str(e['ID']))
                        if p['ESTADOPROCESO_ID']==e['ID']:
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID']==u['ID']:
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

                            json=[{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE":nombreCoachee,
                                "APELLIDO":apellidoCoachee,
                                "CORREO":correoCoachee,
                                "FONO":telefonoCoachee,
                                "CANTSESIONES":cantsesiones,
                                "OBJETIVOS": objetivo,
                                "FECHACREACION": fechaIni,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,  
                                "DESCRIPCION":estadoDescripcion
                                }]

                            listados = json + listados

                    data = {
                    'usuario': perfil,
                    'entity':listados,
                    }
            else:
                    data = {
                    'usuario': perfil,
                    'entity':{'NOMBREEMPRESA':None},
                    }

            return render(request,'procesos/procesosAdmin.html', data)
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)    
    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

#Nuevo Proceso
def nuevoProceso(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            usuarios = requests.get(urlUsuarios,headers=headers).json()
            if request.method == 'POST' and perfil['perfil'] == 1:
                #Obtener datos del Front
                NOMBREEMPRESA = request.POST.get('nombreEmpre')
                CANTSESIONES = request.POST.get('cantiSesiones')
                OBJETIVOS = None
                INDICADORES = None
                PLANACCION = None
                ADMINISTRADOR_ID = '1'
                COACH_ID = request.POST.get('coachProces')
                COACHEE_ID = request.POST.get('coacheeProces')
                    
                #Creo Json 
                json={
                    "NOMBREEMPRESA": NOMBREEMPRESA.title(),
                    "CANTSESIONES": CANTSESIONES,
                    "OBJETIVOS": OBJETIVOS,
                    "INDICADORES": INDICADORES,
                    "PLANACCION": PLANACCION,
                    "ADMINISTRADOR_ID": ADMINISTRADOR_ID,
                    "COACH_ID": COACH_ID,
                    "COACHEE_ID": COACHEE_ID
                    }
                #Metodo para crear usuario en API        
                url = 'http://127.0.0.1:8001/procesos'
                response =  requests.post(url,headers=headers,json=json)

                if response.status_code == 201:
                    #mensaje para avisar al front que se creo el usuario.
                    messages.success(request, 'Proceso creado con éxito.')
                    return redirect('nuevoProceso')
                else:
                    messages.error(request, 'Hubo un problema al crear el proceso.')
                    return redirect('nuevoProceso')

            data = {
                'usuario': perfil,
                'list_usuario':usuarios,
                }

            return render(request,'procesos/nuevoProceso.html', data) 
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)
    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

#listar Proceso
def buscaProceso(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID'
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstadosProcesos = 'http://127.0.0.1:8001/estados-procesos'
            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstadosProcesos,headers=headers).json()
            listados = []
            
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID']==e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID']==u['ID']:
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
                    if p['COACH_ID'] ==uc['ID']:
                        nombreCoach= uc['NOMBRE']
                        apellidoCoach= uc['APELLIDO']

                        json=[{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE":nombreCoachee,
                            "APELLIDO":apellidoCoachee,
                            "CORREO":correoCoachee,
                            "FONO":telefonoCoachee,
                            "FECHACREACION":fechaCreacion,
                            "CANTSESIONES":cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,  
                            "DESCRIPCION":estadoDescripcion,
                            "NOMBRECOACH":nombreCoach,
                            "APELLIDOCOACH":apellidoCoach,
                            "ID": idProceso
                            }]

                        listados = json + listados

            data = {
                'usuario': perfil,
                'entity':listados,
            
            }
            return render(request,'procesos/buscaProceso.html',data)   
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla) 

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

#modificar Proceso
def modProceso(request,id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            if request.method == 'POST':
                ID = id
                NOMBREEMPRESA = request.POST.get('nombreEmpresa')
                CANTSESIONES = request.POST.get('cantidadSesiones')
                OBJETIVOS = ''
                INDICADORES = ''
                PLANACCION = ''
                FECHACREACION = request.POST.get('fechaCreacion')
                FECHATERMINO = None
                ACTIVO = 1
                ESTADOPROCESO_ID = 1
                ADMINISTRADOR_ID = 1
                COACH_ID = 5
                COACHEE_ID = 4

                modificarProcesoJson={
                        "ID": ID,
                        "NOMBREEMPRESA": NOMBREEMPRESA.title(),
                        "CANTSESIONES": CANTSESIONES,
                        "FECHACREACION":FECHACREACION,
                        #"ACTIVO": ACTIVO,
                        #"ESTADOPROCESO_ID": ESTADOPROCESO_ID,
                        "ADMINISTRADOR_ID": ADMINISTRADOR_ID,
                        #"COACH_ID": COACH_ID,
                        #"COACHEE_ID": COACHEE_ID
                        }
                
                modProceso = 'http://127.0.0.1:8001/procesos/'+ str(id) +'/'
                response =  requests.put(modProceso,json=modificarProcesoJson,headers=headers)
                
                if response.status_code == 200:
                    #mensaje para avisar al front que se modifico el proceso.
                    messages.success(request, 'Proceso modificado con éxito.')
                    return redirect('buscaProceso')
                else:
                    messages.error(request, 'Hubo un problema al modificar el proceso.')
                    return redirect('buscaProceso')

            return redirect('buscaProceso') 
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

#información Proceso
def visInfoProceso(request, id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID='+str(id)
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstadosProcesos = 'http://127.0.0.1:8001/estados-procesos'
            urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)
            urlEstadoSesion = 'http://127.0.0.1:8001/estados-sesiones'
            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstadosProcesos,headers=headers).json()
            sesiones = requests.get(urlSesiones,headers=headers).json()
            estadoSesion = requests.get(urlEstadoSesion,headers=headers).json()
            listados = []
            
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID']==e['ID']:
                        idProcesoEstado = p['ESTADOPROCESO_ID']
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID']==u['ID']:
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
                    if p['COACH_ID'] ==uc['ID']:
                        nombreCoach= uc['NOMBRE']
                        apellidoCoach= uc['APELLIDO']

                        json=[{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE":nombreCoachee,
                            "APELLIDO":apellidoCoachee,
                            "CORREO":correoCoachee,
                            "FONO":telefonoCoachee,
                            "FECHACREACION":fechaCreacion,
                            "CANTSESIONES":cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,  
                            "DESCRIPCION":estadoDescripcion,
                            "NOMBRECOACH":nombreCoach,
                            "APELLIDOCOACH":apellidoCoach,
                            "ID": idProceso,
                            "IDESTADOPROCESO": idProcesoEstado
                            }]

                        listados = json + listados
            
            sesiones = sesiones
            estadoSesion = estadoSesion
            print(sesiones)
            data = {
                'usuario': perfil,
                'entity':listados,
                'sesiones':sesiones,
                'estadosSesion':estadoSesion
            }
            
            return render(request,'procesos/visInfoProceso.html',data)   
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla) 

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

#Finalizar un proceso
def finProceso(request,id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            urlProcesos = 'http://127.0.0.1:8001/procesos/'+str(id)+'/'
            
            finProcesoJson ={
                "ID":id,
                "ESTADOPROCESO_ID":6 
                }
            print(finProcesoJson)
            response =  requests.put(urlProcesos,json=finProcesoJson,headers=headers)
            print(response)
            if response.status_code == 200:
                #mensaje para avisar al front que se modifico el proceso.
                messages.success(request, 'Proceso finalizado con éxito.')
                return redirect('buscaProceso')
            elif response.status_code == 409:
                messages.warning(request, 'El proceso ya está finalizado.')
                return redirect('buscaProceso')
            else:
                messages.error(request, 'Hubo un problema al finalizar el proceso.')
                return redirect('buscaProceso')
            #return redirect('buscaProceso')
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla) 

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')    


## ----------------------------------- USUARIOS ------------------------------------------

#usuarios admin Principal
def usuariosAdmin(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            urlCoach = 'http://127.0.0.1:8001/usuarios?ordering=-ID&limit=5&PERFIL_ID=2'
            urlCoachee = 'http://127.0.0.1:8001/usuarios?ordering=-ID&limit=5&PERFIL_ID=3'

            list_coachs = requests.get(urlCoach, headers=headers).json()
            list_coachees = requests.get(urlCoachee, headers=headers).json()

            data ={
                'usuario': perfil,
                'list_coachs':list_coachs,
                'list_coachees':list_coachees
                }

            return render(request,'usuarios/usuariosAdmin.html', data) 
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/') 


#nuevo usuario
def nuevoUsuario(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            data = {
                    'usuario': perfil
                    }
            #Crear usuario
            if request.method == 'POST' and perfil['perfil'] == 1:
                #Obtener datos del Front
                APELLIDO = request.POST.get('apellido')
                CORREO = request.POST.get('email')
                FONO = request.POST.get('telefono')
                IDIOMA = request.POST.get('idioma')
                #Se definen por defecto en None
                EMPRESA = ""
                NOMBREJEFE = ""
                APELLIDOJEFE = ""
                EMAILJEFE = ""
                FONOJEFE = ""
                #Por defecto Activo
                ACTIVO = 1
                #Obtiene tipo de usuario
                if 'nombreCoachee' in request.POST:
                    #Asigno Perfil
                    PERFIL_ID = 3
                    NOMBRE = request.POST.get('nombreCoachee')
                    EMPRESA = request.POST.get('nombreEmp')
                    NOMBREJEFE = request.POST.get('nombreJefe')
                    APELLIDOJEFE = request.POST.get('apellidoJefe')
                    EMAILJEFE = request.POST.get('emailJefe')
                    FONOJEFE = request.POST.get('telefonoJefe')
                
                elif 'nombreCoach' in request.POST:
                    #Asigno Perfil
                    PERFIL_ID = 2
                    NOMBRE = request.POST.get('nombreCoach')
                    
                else:
                    #Usuario Administrador
                    #Asigno Perfil
                    PERFIL_ID = 1
                    NOMBRE = request.POST.get('nombreAdmin')
                    
                #Creo Json 
                crearUsuariosJson={
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

                                
                #Metodo para crear usuario en API        
                urlCrearUsuarios = 'http://127.0.0.1:8001/usuarios'
                response =  requests.post(urlCrearUsuarios, headers=headers,json=crearUsuariosJson)
                
                if response.status_code == 201:
                    #mensaje para avisar al front que se creo el usuario.
                    messages.success(request, 'Usuario creado con éxito.')
                    return render(request,'usuarios/nuevoUsuario.html', data)
                else:
                    messages.error(request, 'Hubo un problema al crear el usuario.')
                
            return render(request,'usuarios/nuevoUsuario.html', data) 
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/') 

#lista usuario
def listUsuarios(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            # print (str(request.session['Perfil_Usuario']))
            # print(str(perfil))
            urlListarUsuarios = 'http://127.0.0.1:8001/usuarios'
            usuarios = requests.get(urlListarUsuarios, headers=headers).json()
            
            data = {
                'usuario': perfil,
                'entity': usuarios,
            }

            return render(request, 'usuarios/listUsuarios.html', data)
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/') 


#Modifica usuario
def modUsuarios(request,id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 1:
            if request.method == 'POST':
                #Obtener datos del Front
                APELLIDO = request.POST.get('apellido')
                CORREO = request.POST.get('email')
                FONO = request.POST.get('telefono')
                IDIOMA = request.POST.get('idioma')
                #Se definen por defecto en None
                EMPRESA = None
                NOMBREJEFE = None
                EMAILJEFE = None
                FONOJEFE = None
                #Por defecto Activo
                estado = request.POST.get('activo')
                if 'activo' in request.POST:
                    ACTIVO = 1
                else:
                    ACTIVO = 0
                
                #Obtiene tipo de usuario
                if 'nombreCoachee' in request.POST:
                    #Asigno Perfil
                    PERFIL_ID = 3
                    NOMBRE = request.POST.get('nombreCoachee')
                    EMPRESA = request.POST.get('nombreEmp')
                    NOMBREJEFE = request.POST.get('nombrejefe')
                    EMAILJEFE = request.POST.get('emailjefe')
                    FONOJEFE = request.POST.get('telefonoJefe')
                
                elif 'nombreCoach' in request.POST:
                #Asigno Perfil
                    PERFIL_ID = 2
                    NOMBRE = request.POST.get('nombreCoach')
                    
                else:
                    #Usuario Administrador
                    #Asigno Perfil
                    PERFIL_ID = 1
                    NOMBRE = request.POST.get('nombreAdmin')
                                
                    
                #Creo Json 
                modificaUsuarioJson={
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
                
                #Metodo para modificar usuario en API        
                urlModUsuarios = 'http://127.0.0.1:8001/usuarios/'+ str(id) +'/'
                response =  requests.put(urlModUsuarios, headers=headers,json=modificaUsuarioJson)

                if response.status_code == 200:
                    messages.success(request, 'Usuario actualizado con éxito.')
                    return redirect('listUsuarios')

                else:
                    messages.error(request, 'Hubo un problema al actualizar el usuario.')
                    return redirect('listUsuarios')

            return redirect('listUsuarios')
        else:
            if perfil['perfil']  == 2:
                plantilla='menuCoach'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')  

# ------------------------ Perteneciente al Coach ------------------------------

# #listar Proceso Coach 
def listProCoach(request):
    try:
        headers = request.session['Headers']
        #print(headers)
        perfil = request.session['Perfil_Usuario']
        
        if perfil['perfil'] == 2:
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&COACH_ID='+str(perfil['id'])
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstado,headers=headers).json()
            
            listados = []

            #listado = proceso.update(usuario)
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID']==e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID']==u['ID']:
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
                    if p['COACH_ID'] ==uc['ID']:
                        nombreCoach= uc['NOMBRE']
                        apellidoCoach= uc['APELLIDO']

                        json=[{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE":nombreCoachee,
                            "APELLIDO":apellidoCoachee,
                            "CORREO":correoCoachee,
                            "FONO":telefonoCoachee,
                            "FECHACREACION":fechaCreacion,
                            "CANTSESIONES":cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,  
                            "DESCRIPCION":estadoDescripcion,
                            "NOMBRECOACH":nombreCoach,
                            "APELLIDOCOACH":apellidoCoach,
                            "ID": idProceso
                            }]

                        listados = json + listados

            data = {
                'usuario': perfil,
                'entity':listados,
            }
          

            return render(request,'procesoCoach/listProCoach.html',data)
        
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/') 


#Procesos asignados al Coach
def procAsig(request):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 2:
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ESTADOPROCESO_ID=1&COACH_ID='+str(perfil['id'])
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstado,headers=headers).json()
            listados = []

            #listado = proceso.update(usuario)
            if len(proceso) > 0:
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID']==e['ID']:
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID']==u['ID']:
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
                        if p['COACH_ID'] ==uc['ID']:
                            nombreCoach= uc['NOMBRE']
                            apellidoCoach= uc['APELLIDO']

                            json=[{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE":nombreCoachee,
                                "APELLIDO":apellidoCoachee,
                                "CORREO":correoCoachee,
                                "FONO":telefonoCoachee,
                                "FECHACREACION":fechaCreacion,
                                "CANTSESIONES":cantsesiones,
                                "OBJETIVOS": objetivo,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,  
                                "DESCRIPCION":estadoDescripcion,
                                "NOMBRECOACH":nombreCoach,
                                "APELLIDOCOACH":apellidoCoach,
                                "ID": idProceso
                                }]

                            listados = json + listados

                page = request.GET.get('page',1)

                try:
                    paginator = Paginator(listados,10)
                    listado = paginator.page(page)

                except:
                    raise Http404

                data = {
                    'usuario': perfil,
                    'entity':listado,
                    'paginator':paginator
                }
            else:
                data = {
                'usuario': perfil,
                'entity':{'NOMBREEMPRESA':None},
                }

            return render(request,'procesoCoach/procAsig.html', data) 
        
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/') 

#Obtener y modificar de los procesos coach
def infoProcCoach(request,id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 2:
            if request.method == 'POST':
                #print('FORMULARIO PROCESO')
                """ nombreEmpresa = request.POST.get('nombre')
                nombreCoachee = request.POST.get('nombre')
                apellidoCoachee = request.POST.get('nombre')
                correoCoachee = request.POST.get('nombre')
                telefonoCoachee = request.POST.get('nombre')
                fechaCreacion = request.POST.get('nombre')
                cantsesiones = request.POST.get('nombre') """
                objetivo = request.POST.get('objetivosProc')
                indicadores = request.POST.get('indicadoresProc')
                planAccion = request.POST.get('planAccionProc')
                """ nombreJefe = request.POST.get('nombre')
                emailJefe = request.POST.get('nombre')
                fonoJefe = request.POST.get('nombre')
                estadoDescripcion = request.POST.get('nombre')
                nombreCoach = request.POST.get('nombre')
                apellidoCoach = request.POST.get('nombre') """
                idProceso  = id

                modProcCoach={
                            "ID":idProceso,
                            "OBJETIVOS":objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion
                }
                #print(modProcCoach)
                #Metodo para modificar proceso Coach en API        
                urlModProcesos = 'http://127.0.0.1:8001/procesos/'+ str(id) +'/'
                response =  requests.put(urlModProcesos, headers=headers,json=modProcCoach)
                #print(response.status_code)
                
                if response.status_code == 200:
                    messages.success(request, 'Proceso actualizado con éxito.')
                    return redirect('listProCoach')
                else:
                    messages.error(request, 'Hubo un problema al actualizar el proceso.')
                    return redirect('listProCoach')

            if request.method == 'GET': 
                urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID='+str(id)
                urlUsuarios = 'http://127.0.0.1:8001/usuarios'
                urlEstado = 'http://127.0.0.1:8001/estados-procesos'
                urlEstadoSesion = 'http://127.0.0.1:8001/estados-sesiones'
                proceso = requests.get(urlProcesos,headers=headers).json()
                usuario = requests.get(urlUsuarios,headers=headers).json()
                estado = requests.get(urlEstado,headers=headers).json()
                urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)
                sesiones = requests.get(urlSesiones,headers=headers).json()
                estadoSesion = requests.get(urlEstadoSesion,headers=headers).json()
                listados = []

                #listado = proceso.update(usuario)
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID']==e['ID']:
                            idProcesoEstado = p['ESTADOPROCESO_ID']
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID']==u['ID']:
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
                        if p['COACH_ID'] ==uc['ID']:
                            nombreCoach= uc['NOMBRE']
                            apellidoCoach= uc['APELLIDO']

                            json=[{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE":nombreCoachee,
                                "APELLIDO":apellidoCoachee,
                                "CORREO":correoCoachee,
                                "FONO":telefonoCoachee,
                                "FECHACREACION":fechaCreacion,
                                "CANTSESIONES":cantsesiones,
                                "OBJETIVOS": objetivo,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,  
                                "DESCRIPCION":estadoDescripcion,
                                "NOMBRECOACH":nombreCoach,
                                "APELLIDOCOACH":apellidoCoach,
                                "ID": idProceso,
                                "IDESTADOPROCESO": idProcesoEstado
                                }]
                    
                            listados = json + listados
                
                sesiones = sesiones
                estado = estado
                estadoSesion = estadoSesion
                #print(sesiones)
                #print(estado)
                data = {
                    'usuario': perfil,
                    'entity':listados,
                    'sesiones':sesiones,
                    'estados':estado,
                    'estadosSesion':estadoSesion
                }

                return render(request,'procesoCoach/infoProcCoach.html',data)
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

#Modificar sesiones Coach
def infoSesionCoach(request,id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 2:
            idP =  request.POST.get('proceso')
            if request.method == 'POST':
                #idP =  request.POST.get('proceso')
                FECHASESION = request.POST.get('fechaSesion')
                HORASESION = request.POST.get('horaSesion')
                DESCRIPCION = request.POST.get('descSesion')
                AVANCES = request.POST.get('asigSesion')
                ASIGNACION = request.POST.get('avancesSesion')
                #ACTIVO = request.POST.get('nombreCoachee')
                ESTADOSESION_ID = request.POST.get('estadoSesion1')
                                
                modificarSesionesJson= {
                        "ID": int(id),
                        "FECHASESION": FECHASESION,
                        "HORASESION": HORASESION,
                        "DESCRIPCION": DESCRIPCION,
                        "AVANCES": AVANCES,
                        "ASIGNACION": ASIGNACION,
                        #"ACTIVO": 1,
                        "PROCESO_ID": int(idP),
                        "ESTADOSESION_ID": int(ESTADOSESION_ID)
                        }

                print(modificarSesionesJson)
                urlSesiones = 'http://127.0.0.1:8001/sesiones/'+str(id)+'/'
                response =  requests.put(urlSesiones, headers=headers,json=modificarSesionesJson)
                print(response)
                if response.status_code == 200:
                    messages.success(request, 'Sesión actualizada con éxito.')
                    return redirect('infoProcCoach',idP)
                else:
                    messages.error(request, 'Hubo un problema al actualizar la sesión.')
                    return redirect('infoProcCoach',idP)
            return redirect('listProCoach')
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)
    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

# ------------------------------  Perteneciente al Coachee ----------------------------------------------#

#Procesos asignados al Coachee
def infoProCoachee(request, id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 3:
            if request.method == 'GET': 
                urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID='+str(id)
                urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)
                urlUsuarios = 'http://127.0.0.1:8001/usuarios'
                urlEstado = 'http://127.0.0.1:8001/estados-procesos'
                urlEstadoSesion = 'http://127.0.0.1:8001/estados-sesiones'
                proceso = requests.get(urlProcesos,headers=headers).json()
                usuario = requests.get(urlUsuarios,headers=headers).json()
                estado = requests.get(urlEstado,headers=headers).json()
                sesiones = requests.get(urlSesiones,headers=headers).json()
                estadoSesion = requests.get(urlEstadoSesion,headers=headers).json()
                listados = []
                print(sesiones)
                #listado = proceso.update(usuario)
                for p in proceso:
                    for e in estado:
                        if p['ESTADOPROCESO_ID']==e['ID']:
                            idProcesoEstado = p['ESTADOPROCESO_ID']
                            estadoDescripcion = e['DESCRIPCION']
                    for u in usuario:
                        if p['COACHEE_ID']==u['ID']:
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
                        if p['COACH_ID'] ==uc['ID']:
                            nombreCoach= uc['NOMBRE']
                            apellidoCoach= uc['APELLIDO']
            
                            json=[{
                                "NOMBREEMPRESA": nombreEmpresa,
                                "NOMBRE":nombreCoachee,
                                "APELLIDO":apellidoCoachee,
                                "CORREO":correoCoachee,
                                "FONO":telefonoCoachee,
                                "FECHACREACION":fechaCreacion,
                                "CANTSESIONES":cantsesiones,
                                "OBJETIVOS": objetivo,
                                "INDICADORES": indicadores,
                                "PLANACCION": planAccion,
                                "NOMBREJEFE": nombreJefe,
                                "EMAILJEFE": emailJefe,
                                "FONOJEFE": fonoJefe,  
                                "DESCRIPCION":estadoDescripcion,

                                "NOMBRECOACH":nombreCoach,
                                "APELLIDOCOACH":apellidoCoach,
                                "IDESTADOPROCESO": idProcesoEstado,
                                "ID": idProceso
                                }]
                    
                            listados = json + listados
                
                sesiones = sesiones
                estado = estado
                estadoSesion = estadoSesion
                data = {
                    'usuario': perfil,
                    'entity':listados,
                    'sesiones':sesiones,
                    'estados':estado,
                    'estadosSesion':estadoSesion
                }
          
                return render(request,'procesoCoachee/infoProCoachee.html',data)
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 2:
                plantilla='menuCoach'
            return redirect(plantilla) 

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')

#Imprimi Reporte

def imprimirProceso(request,id):
    try:
        headers = request.session['Headers']
        perfil = request.session['Perfil_Usuario']
        if perfil['perfil'] == 2 or perfil['perfil'] == 1:
            urlProcesos = 'http://127.0.0.1:8001/procesos?ordering=-ID&ID='+str(id)
            urlUsuarios = 'http://127.0.0.1:8001/usuarios'
            urlEstado = 'http://127.0.0.1:8001/estados-procesos'
            urlSesiones = 'http://127.0.0.1:8001/sesiones?PROCESO_ID='+str(id)
            proceso = requests.get(urlProcesos,headers=headers).json()
            usuario = requests.get(urlUsuarios,headers=headers).json()
            estado = requests.get(urlEstado,headers=headers).json()
            sesiones = requests.get(urlSesiones,headers=headers).json()
            listados = []

            #listado = proceso.update(usuario)
            for p in proceso:
                for e in estado:
                    if p['ESTADOPROCESO_ID']==e['ID']:
                        estadoDescripcion = e['DESCRIPCION']
                for u in usuario:
                    if p['COACHEE_ID']==u['ID']:
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
                    if p['COACH_ID'] ==uc['ID']:
                        nombreCoach= uc['NOMBRE']
                        apellidoCoach= uc['APELLIDO']
                        correoCoach= uc['CORREO']
                        fonoCoach= uc['FONO']

                        json=[{
                            "NOMBREEMPRESA": nombreEmpresa,
                            "NOMBRE":nombreCoachee,
                            "APELLIDO":apellidoCoachee,
                            "CORREO":correoCoachee,
                            "FONO":telefonoCoachee,
                            "FECHACREACION":fechaCreacion,
                            "FECHATERMINO":fechaTermino,
                            "CANTSESIONES":cantsesiones,
                            "OBJETIVOS": objetivo,
                            "INDICADORES": indicadores,
                            "PLANACCION": planAccion,
                            "NOMBREJEFE": nombreJefe,
                            "EMAILJEFE": emailJefe,
                            "FONOJEFE": fonoJefe,  
                            "DESCRIPCION":estadoDescripcion,
                            "NOMBRECOACH":nombreCoach,
                            "APELLIDOCOACH":apellidoCoach,
                            "CORREOCOACH":correoCoach,
                            "FONOCOACH":fonoCoach,
                            "ID": idProceso
                            }]

                        listados = json + listados
            
            template = get_template("base/reporte.html")
            
            data = {
                'usuario': perfil,
                'entity':listados,
                'sesiones':sesiones
            }
            context = {
                 'entity':listados,
                 'sesiones':sesiones
            }
            html_template = template.render(context)
            css_url = os.path.join(settings.BASE_DIR,'frontProject/static/css/bootstrap.css')
            
            pdf_file = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])
            
            response = HttpResponse(pdf_file,content_type='application/pdf;')
            response['Content-Disposition'] = 'inline; filename=reporte_proceso.pdf'
            #with open("reporte_proceso.pdf", "rb") as pdf_file:
            #    encoded_string = base64.b64encode(pdf_file)
            #    pdf_file.close()
            encoded = base64.b64encode(pdf_file)
            response['Content-Transfer-Encoding'] = 'binary'
            response['Content-Disposition'] = 'attachment; filename= ReporteEmpresa_'+ nombreEmpresa + '.pdf'
            return response
            #return render(request,'procesoCoach/infoProcCoach.html',data)
        else:
            if perfil['perfil']  == 1:
                plantilla='menuAdmin'
            elif perfil['perfil']  == 3:
                plantilla='menuCoachee'
            return redirect(plantilla)

    except Exception as e:
        messages.warning(request,'Ingrese sus credenciales para acceder')
        return redirect('/')
