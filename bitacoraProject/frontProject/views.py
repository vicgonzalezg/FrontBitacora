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
from django.template import loader

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

        if r.status_code == 200:
            result = json.loads(r.content) 
            print(result)
            nombre_usuario=result['USUARIO']['NOMBRE']+' '+result['USUARIO']['APELLIDO']
            perfil_usuario=result['USUARIO']['PERFIL_ID']
            id_usuario = result['USUARIO']['ID']
            datos_usuario={'nombre': nombre_usuario,'perfil':perfil_usuario,'id':id_usuario}
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
            plantilla=''
            if perfil_usuario==1:
                plantilla='menu/menuAdmin.html'
            elif perfil_usuario==2:
                plantilla='menu/menuCoach.html'
            elif perfil_usuario==3:
                plantilla='menu/menuCoachee.html'
            return render(request,plantilla,{'usuario':datos_usuario})
        else:
            messages.error(request, 'Usuario y/o contraseña incorrectos.')
            return render(request, 'login/login.html')
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
#Perfil
def perfil(request):
    perfil = request.session['Perfil_Usuario']
    print(perfil)
    #Buscar la forma de obtener el ID del usuario
    #Lo otro seria pasar el ID del usuario en el request.session
    return render(request,'Perfil/perfil.html',{'usuario': perfil})

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
    url = 'http://127.0.0.1:8001/procesos'
    url2 = 'http://127.0.0.1:8001/usuarios'
    url3 = 'http://127.0.0.1:8001/estados-procesos'
    proceso = requests.get(url).json()
    usuario = requests.get(url2).json()
    estado = requests.get(url3).json()
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
                cantsesiones = p['CANTSESIONES']
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
                    "INDICADORES": indicadores,
                    "PLANACCION": planAccion,
                    "NOMBREJEFE": nombreJefe,
                    "EMAILJEFE": emailJefe,
                    "FONOJEFE": fonoJefe,  
                    "DESCRIPCION":estadoDescripcion
                    }]

                listados = json + listados

    return render(request,'procesos/procesosAdmin.html',{'usuario': perfil,'list_proceso':listados})    


#Nuevo Proceso
def nuevoProceso(request):
    headers = request.session['Headers']
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #print (admin)
    #admin={'nombre': 'María José','perfil':1}
    #Crear usuario
    url2 = 'http://127.0.0.1:8001/usuarios'
    usuarios = requests.get(url2).json()
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
            "NOMBREEMPRESA": NOMBREEMPRESA,
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
        response =  requests.post(url,json=json)
        print(json)
        print(response)
        #if response.status_code == 201:
        #    mensaje para avisar al front que se creo el usuario.

    return render(request,'procesos/nuevoProceso.html',{'usuario': perfil, 'list_usuario':usuarios}) 

#listar Proceso
def buscaProceso(request):
    perfil = request.session['Perfil_Usuario']
    urlProcesos = 'http://127.0.0.1:8001/procesos'
    urlUsuarios = 'http://127.0.0.1:8001/usuarios'
    urlEstadosProcesos = 'http://127.0.0.1:8001/estados-procesos'
    proceso = requests.get(urlProcesos).json()
    usuario = requests.get(urlUsuarios).json()
    estado = requests.get(urlEstadosProcesos).json()
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
                cantsesiones = p['CANTSESIONES']
                objetivo = p['OBJETIVOS']
                indicadores = p['INDICADORES']
                planAccion = p['PLANACCION']
                nombreJefe = u['NOMBREJEFE']
                emailJefe = u['EMAILJEFE']
                fonoJefe = u['FONOJEFE']
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
                    "CANTSESIONES":cantsesiones,
                    "OBJETIVOS": objetivo,
                    "INDICADORES": indicadores,
                    "PLANACCION": planAccion,
                    "NOMBREJEFE": nombreJefe,
                    "EMAILJEFE": emailJefe,
                    "FONOJEFE": fonoJefe,  
                    "DESCRIPCION":estadoDescripcion,
                    "NOMBRECOACH":nombreCoach,
                    "APELLIDOCOACH":apellidoCoach
                    }]

                listados = json + listados

        page = request.GET.get('page', 1)

    try:
        paginator = Paginator(listados, 10)
        lista = paginator.page(page)
    except:
        raise Http404

    data = {
        'usuario': perfil,
        'entity':lista,
        'paginator': paginator
    }
    print(p)
    return render(request,'procesos/buscaProceso.html',data)        


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

## ----------------------------------- USUARIOS ------------------------------------------

#usuarios admin
def usuariosAdmin(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    #admin={'nombre': 'María José','perfil':1}
    urlCoach = 'http://127.0.0.1:8001/usuarios?ordering=-ID&limit=5&PERFIL_ID=2'
    urlCoachee = 'http://127.0.0.1:8001/usuarios?ordering=-ID&limit=5&PERFIL_ID=3'
    list_coachs = requests.get(urlCoach).json()
    print(list_coachs)
    list_coachees = requests.get(urlCoachee).json()
    print(list_coachees)
    return render(request,'usuarios/usuariosAdmin.html',{'usuario': perfil,'list_coachs':list_coachs,'list_coachees':list_coachees}) 


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
        #NOMBRE = request.POST.get('nombre')
        #SNOMBRE = request.POST.get('idProd')
        APELLIDO = request.POST.get('apellido')
        #SAPELLIDO = request.POST.get('idProd')
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
                    #"SNOMBRE": None, #Se envia null
                    "APELLIDO": APELLIDO,
                    #"SAPELLIDO": None, #Se envia null
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
        response =  requests.post(urlCrearUsuarios,json=crearUsuariosJson)
        print(crearUsuariosJson)
        print(response)
        
        if response.status_code == 201:
            #mensaje para avisar al front que se creo el usuario.
            messages.success(request, 'Usuario creado con éxito.')
            return render(request,'usuarios/nuevoUsuario.html',{'usuario': perfil})
        else:
            messages.error(request, 'Hubo un problema al crear el usuario.')

    return render(request,'usuarios/nuevoUsuario.html',{'usuario': perfil}) 


#lista usuario
# lista usuario
def listUsuarios(request):
    headers = request.session['Headers']
    perfil = request.session['Perfil_Usuario']
    # print (str(request.session['Perfil_Usuario']))
    # print(str(perfil))
    urlListarUsuarios = 'http://127.0.0.1:8001/usuarios'
    usuarios = requests.get(urlListarUsuarios).json()
    # Paginacion
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(usuarios, 5)
        usuario = paginator.page(page)
    except:
        raise Http404

    data = {
        'usuario': perfil,
        'entity': usuario,
        'paginator': paginator
    }
    return render(request, 'usuarios/listUsuarios.html', data)

#Modifica usuario
def modUsuarios(request,id):
    headers = request.session['Headers']
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    print(str(perfil))
    print('ID de usuario a modificar: ' + str(id))
    print (request.method)
    if request.method == 'POST' and perfil['perfil'] == 1:
        #Obtener datos del Front
        #NOMBRE = request.POST.get('nombre')
        #SNOMBRE = request.POST.get('idProd')
        APELLIDO = request.POST.get('apellido')
        #SAPELLIDO = request.POST.get('idProd')
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
        #estado2 = request.POST.get('off')
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
                    #"SNOMBRE": None, #Se envia null
                    "APELLIDO": APELLIDO,
                    #"SAPELLIDO": None, #Se envia null
                    "FONO": FONO,
                    "IDIOMA": IDIOMA,
                    "EMPRESA": EMPRESA,
                    "NOMBREJEFE": str(NOMBREJEFE),
                    "EMAILJEFE": EMAILJEFE,
                    "FONOJEFE": FONOJEFE,
                    "ACTIVO": ACTIVO,
                    "PERFIL_ID": PERFIL_ID
                    }

        
        print(str(modificaUsuarioJson))
        
        #Metodo para crear usuario en API        
        urlModUsuarios = 'http://127.0.0.1:8001/usuarios/'+ str(id) +'/'
        response =  requests.put(urlModUsuarios,json=modificaUsuarioJson)
        print(response)

        if response.status_code == 200:
            messages.success(request, 'Usuario actualizado con éxito.')
            return redirect('listUsuarios')
        else:
            messages.error(request, 'Hubo un problema al actualizar el usuario.')
            return redirect('listUsuarios')

    return redirect('listUsuarios') 

#Buscar usuarios
def buscaUsuarios(request):
    headers = request.session['Headers']
    perfil = request.session['Perfil_Usuario']
    url = 'http://127.0.0.1:8001/usuarios?ordering=ID'
    if request.method == 'POST':
        tipoUsuario = request.POST.get('tipoUsuario')
        print(tipoUsuario)
        estadoUsuario = request.POST.get('estado')
        print(estadoUsuario)
        #TipoUsuarios = Todos & Estado = Todos
        if tipoUsuario=='0' and estadoUsuario=='2':
            return redirect('listUsuarios') 
        #TipoUsuarios = Administrador o Coach o Coachee & Estado = Todos
        elif tipoUsuario=='1' and estadoUsuario=='2' or tipoUsuario=='2' and estadoUsuario=='2' or tipoUsuario=='3' and estadoUsuario=='2':
            url = url + '&PERFIL_ID=' + str(tipoUsuario) 
            print(url)
            usuario = requests.get(url).json()
            return render(request,'usuarios/listUsuarios.html',{'usuario': perfil,'list_usuarios':usuario,'tipousuario':tipoUsuario,'estadoUsuario':estadoUsuario})
        #TipoUsuarios = Todos & Estado = Activo o Inactivo
        elif tipoUsuario=='0' and estadoUsuario=='0' or tipoUsuario=='0' and estadoUsuario=='1':
            url = url + '&ACTIVO=' + str(estadoUsuario) 
            print(url)
            usuario = requests.get(url).json()
            return render(request,'usuarios/listUsuarios.html',{'usuario': perfil,'list_usuarios':usuario,'tipousuario':tipoUsuario,'estadoUsuario':estadoUsuario})
        #Mezcla de Tipos de usuarios o estado
        else:
            url = url + '&PERFIL_ID=' + str(tipoUsuario) + '&ACTIVO=' + str(estadoUsuario) 
            print(url)
            usuario = requests.get(url).json()
            return render(request,'usuarios/listUsuarios.html',{'usuario': perfil,'list_usuarios':usuario,'tipousuario':tipoUsuario,'estadoUsuario':estadoUsuario})
    return redirect('listUsuarios') 

#estado usuario
def estadoUsuarios(request):
    perfil = request.session['Perfil_Usuario']
    print (str(request.session['Perfil_Usuario']))
    admin={'nombre': 'María José','perfil':1}
    return render(request,'usuarios/estadoUsuarios.html',{'usuario': perfil})




# ------------------------ Perteneciente al Coach ------------------------------

# #listar Proceso
def listProCoach(request):
    #perfil = request.session['Perfil_Usuario']
    #print (str(request.session['Perfil_Usuario']))
    coach={'nombre': 'Nelson Gomez','perfil':2}
    return render(request,'procesoCoach/listProCoach.html',{'usuario': coach})


#Procesos asignados al Coach
def procAsig(request):
    #perfil = request.session['Perfil_Usuario']
    #print (str(request.session['Perfil_Usuario']))
    coach={'nombre': 'Nelson Gomez','perfil':2}
    return render(request,'procesoCoach/procAsig.html',{'usuario': coach}) 


#Perteneciente al Coachee

#Procesos asignados al Coachee
def infoProCoachee(request):
    #perfil = request.session['Perfil_Usuario']
    #print (str(request.session['Perfil_Usuario']))
    coach={'nombre': 'Victor Gonzalez','perfil':3}
    return render(request,'procesoCoachee/infoProCoachee.html',{'usuario': coach})


