from frontProject.models import Usuario
from django.shortcuts import render, redirect
from django.http import HttpResponse, response
import requests
from . import services
# Create your views here.
from django.core import serializers
import json
import requests
#definimos el login
def login(request):
    if request.method == 'POST':
        #admin={'nombre': 'María José','perfil':1}
        #coach={'nombre': 'Nelson Gomez','perfil':2}
        #coachee={'nombre': 'Victor Gonzalez','perfil':3}
        username = request.POST.get('user')
        password = request.POST.get('pass')
        print(username,password)
        #r=services.LoginServices().generate_request(username,password)
        r = requests.post('http://127.0.0.1:8001/login', data = {'USUARIO':username,'CONTRASENA':password})
        print(r.content)

        result = json.loads(r.content) 
        print(result)

        nombre_usuario=result['USUARIO']['NOMBRE']+' '+result['USUARIO']['APELLIDO']
        perfil_usuario=result['USUARIO']['PERFIL_ID']
        datos_usuario={'nombre': nombre_usuario,'perfil':perfil_usuario}
        token = result['TOKEN']
        print('Hola soy un token: '+ token)
        headers = {
                'content-type': "application/json",
                'authorization': "Bearer " + token
            }
        request.session['Headers'] = headers
        
        request.session['Perfil_Usuario'] = datos_usuario
        print(datos_usuario)
        print(str(request.session['Headers']))
        print(str(request.session['Perfil_Usuario']))
        if r.status_code == 200:
            plantilla=''
            if perfil_usuario==1:
                plantilla='menu/menuAdmin.html'
            elif perfil_usuario==2:
                plantilla='menu/menuCoach.html'
            elif perfil_usuario==3:
                plantilla='menu/menuCoachee.html'
            return render(request,plantilla,{'usuario':datos_usuario})
        #if username == 'maria.jose' and password == 'inicio2021':
            #return render(request,'menu/menuAdmin.html',{'usuario': admin})
        #elif username== 'nelson.gomez' and password == 'inicio2021':
            #return render(request,'menu/menuCoach.html',{'usuario': coach})
        #elif username== 'victor.gonzalez' and password == 'inicio2021':
        #    return render(request,'menu/menuCoachee.html',{'usuario': coachee})
    return render(request, 'login/login.html')

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
#Menu
#def menu(request):
    #if request.method == 'POST':
        #username = request.POST.get('user')
        #password = request.POST.get('pass')
        #print(username,password)
        #if username == 'maria.jose' and password == 'inicio2021':
        #    return render(request,'menu/menuAdmin.html')
        #elif username== 'juan.topo' and password == 'inicio2021':
        #    return render(request,'menu/menuCoach.html')

#    return render(request, 'login/login.html')

#Paginas de Menu por Peril
def menuAdmin(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'menu/menuAdmin.html',{'usuario': admin})

def menuCoach(request):
    coach={'nombre': 'Nelson Gomez','perfil':2}
    return render(request,'menu/menuCoach.html',{'usuario': coach})


def menuCoachee(request):
    coachee={'nombre': 'Victor Gonzalez','perfil':3}
    return render(request,'menu/menuCoachee.html',{'usuario': coachee})

#Proceso
#def procesos(request):
#    return render(request, 'login/login.html')

#Perteneciente al administrador

#Paginas de Procesos
def procesosAdmin(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/procesosAdmin.html',{'usuario': perfil})

#Nuevo Proceso
def nuevoProceso(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/nuevoProceso.html',{'usuario': perfil})

#modificar Proceso
def buscaProceso(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/buscaProceso.html',{'usuario': perfil})   

#modificar Proceso
def modProceso(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/modProceso.html',{'usuario': perfil})    


#listar Proceso
def listProceso(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/listProceso.html',{'usuario': perfil})

#terminar Proceso
def termiProceso(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/termiProceso.html',{'usuario': perfil})  

#información Proceso
def infoProceso(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/infoProceso.html',{'usuario': perfil})  

#usuarios admin
def usuariosAdmin(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/usuariosAdmin.html',{'usuario': perfil}) 

#nuevo usuario
def nuevoUsuario(request):
    headers = request.session['Headers']
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #print (admin)
    #admin={'nombre': 'María José','perfil':1}
    #Crear usuario
    if request.method == 'POST' and perfil['perfil'] == 1:
        #Obtener datos del Front
        NOMBRE = request.POST.get('nombre')
        #SNOMBRE = request.POST.get('idProd')
        APELLIDO = request.POST.get('apellido')
        #SAPELLIDO = request.POST.get('idProd')
        CORREO = request.POST.get('email')
        FONO = request.POST.get('telefono')
        IDIOMA = request.POST.get('idioma')
        EMPRESA = request.POST.get('nombreEmp')
        NOMBREJEFE = request.POST.get('nombreJefe')
        APELLIDOJEFE = request.POST.get('apellidoJefe')
        EMAILJEFE = request.POST.get('emailJefe')
        FONOJEFE = request.POST.get('telefonoJefe')
        #Por defecto Activo
        ACTIVO = 1
        #Por defecto Coachee
        PERFIL_ID = 2
        #Usuario Coach
        usuarioCoachee = request.POST.get('coachee')
        print(usuarioCoachee)
        if usuarioCoachee == 'coachee':
            #Asigno Perfil
            PERFIL_ID = 3
            #Creo Json Coachee
            json={
                    "USUARIO": NOMBRE.lower()+'.'+APELLIDO.lower(),
                    "NOMBRE": NOMBRE,
                    #"SNOMBRE": None, #Se envia null
                    "APELLIDO": APELLIDO,
                    #"SAPELLIDO": None, #Se envia null
                    "CORREO": CORREO,
                    "FONO": FONO,
                    "IDIOMA": IDIOMA,
                    "EMPRESA": EMPRESA,
                    "NOMBREJEFE": str(NOMBREJEFE)+' '+str(APELLIDOJEFE),
                    "EMAILJEFE": EMAILJEFE,
                    "FONOJEFE": FONOJEFE,
                    "ACTIVO": ACTIVO,
                    "PERFIL_ID": PERFIL_ID
                    }
        elif PERFIL_ID == 2:
            #Usuario Coach
            json={
                    "USUARIO": NOMBRE.lower()+'.'+APELLIDO.lower(),
                    "NOMBRE": NOMBRE,
                    #"SNOMBRE": None, #Se envia null
                    "APELLIDO": APELLIDO,
                    #"SAPELLIDO": None, #Se envia null
                    "CORREO": CORREO,
                    "FONO": FONO,
                    "IDIOMA": IDIOMA,
                    "ACTIVO": ACTIVO,
                    "PERFIL_ID": PERFIL_ID
                }
        else:
            #Usuario Administrador
            #Asigno Perfil
            PERFIL_ID = 1
            json={
                    "USUARIO": NOMBRE.lower()+'.'+APELLIDO.lower(),
                    "NOMBRE": NOMBRE,
                    #"SNOMBRE": None, #Se envia null
                    "APELLIDO": APELLIDO,
                    #"SAPELLIDO": None, #Se envia null
                    "CORREO": CORREO,
                    "FONO": FONO,
                    "IDIOMA": IDIOMA,
                     "ACTIVO": ACTIVO,
                    "PERFIL_ID": PERFIL_ID
                }
        #Metodo para crear usuario en API        
        url = 'http://127.0.0.1:8001/usuarios'
        response =  requests.post(url,json=json)
        print(json)
        print(response)
        #if response.status_code == 201:
        #    mensaje para avisar al front que se creo el usuario.

    return render(request,'usuarios/nuevoUsuario.html',{'usuario': perfil}) 

#lista usuario
def modUsuario(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    url = 'http://127.0.0.1:8001/usuarios'
    usuario = requests.get(url).json()
    print(usuario)
    #admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/modUsuario.html',{'usuario': perfil,'list_usuarios':usuario}) 

#lista usuario
def listUsuarios(request):
    headers = request.session['Headers']
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    print(str(perfil))
    url = 'http://127.0.0.1:8001/usuarios'
    usuario = requests.get(url).json()
    print(usuario)
    #datos_usuario = request.session['Cache']
    #print('Token desde lista usuarios:' + str(headers))
    #print('datos usuario desde lista usuarios:' + str(datos_usuario))
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/listUsuarios.html',{'usuario': perfil,'list_usuarios':usuario}) 

#estado usuario
def estadoUsuarios(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/estadoUsuarios.html',{'usuario': perfil})


#Perteneciente al Coach

#listar Proceso
def listProCoach(request):
    coach={'nombre': 'Nelson Gomez','perfil':2}
    return render(request,'procesoCoach/listProCoach.html',{'usuario': coach})