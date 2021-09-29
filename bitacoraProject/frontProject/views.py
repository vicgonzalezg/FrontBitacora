from frontProject.models import Usuario
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from . import services
# Create your views here.
from django.core import serializers
import json
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
        print(datos_usuario)
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
    admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/procesosAdmin.html',{'usuario': admin})

#Nuevo Proceso
def nuevoProceso(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/nuevoProceso.html',{'usuario': admin})

#modificar Proceso
def buscaProceso(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/buscaProceso.html',{'usuario': admin})   

#modificar Proceso
def modProceso(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/modProceso.html',{'usuario': admin})    


#listar Proceso
def listProceso(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/listProceso.html',{'usuario': admin})

#terminar Proceso
def termiProceso(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/termiProceso.html',{'usuario': admin})  

#información Proceso
def infoProceso(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'procesos/infoProceso.html',{'usuario': admin})  

#usuarios admin
def usuariosAdmin(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/usuariosAdmin.html',{'usuario': admin}) 

#nuevo usuario
def nuevoUsuario(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/nuevoUsuario.html',{'usuario': admin}) 

#lista usuario
def modUsuario(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/modUsuario.html',{'usuario': admin}) 

#lista usuario
def listUsuarios(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/listUsuarios.html',{'usuario': admin}) 

#estado usuario
def estadoUsuarios(request):
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/estadoUsuarios.html',{'usuario': admin})

    #Perteneciente al Coach

#listar Proceso
def listProCoach(request):
    coach={'nombre': 'Nelson Gomez','perfil':2}
    return render(request,'procesoCoach/listProCoach.html',{'usuario': coach})