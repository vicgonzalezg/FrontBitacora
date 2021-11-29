from bitacoraProject.settings import API_ROUTE,FRONT_ROUTE
#Ordenar de A-Z
from . import models
from django.core import serializers
from django.apps import apps
import requests
import json

class ApiCall:

    """    
    def get(url,header):
        r=None
        r=requests.get(API_ROUTE+url,headers=header).json()
        #print(r)
        return r
    """
    def get(url,query,header):
        r=None
        if query is not None:
            r=requests.get(API_ROUTE+url+'?'+query,headers=header).json()
        else:
            r=requests.get(API_ROUTE+url,headers=header).json()
        #print(r)
        return r

    def get_one(url,header,pk):
        r=None
        if pk is not None:
            r=requests.get(API_ROUTE+url+'/'+str(pk),headers=header).json()
        else:
            r=requests.get(API_ROUTE+url,headers=header).json()
        return r

    def post(url,data,header):
        r=None
        print(data)
        if header is not None:
            r=requests.post(API_ROUTE+url,json=data,headers=header)
        else:
            r=requests.post(API_ROUTE+url,json=data)
        return r
    
    """ def postArchivo(url,data,files,header):
        r=None
        print(data)
        if header is not None:
            header['content-type'] = 'application/multipart/form-data'
            print(header)
            r=requests.post(API_ROUTE+url,files=data,headers=header)
        else:
            r=requests.post(API_ROUTE+url,data=data)
        return r """

    def put(url,data,pk,header):
        print(data)
        r=requests.put(API_ROUTE+url+'/'+str(pk)+'/',json=data,headers=header)
        return r
    
    def put_one(url,pk,data):
        print(data)
        r=requests.put(API_ROUTE+url+'/'+str(pk)+'/',json=data)
        return r

    def delete(url,data,pk,header):
        r=requests.delete(API_ROUTE+url+'/'+str(pk),json=data,headers=header)
        print(r)
        return r

def sesionUsuario(request,r):
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
    return perfil_usuario

def currentheaders(request):
    headers = request.session['Headers']
    return headers

def perfilUsuario(request):
    perfil = request.session['Perfil_Usuario']
    return perfil

#Aquellas que no estan restringidas por token
class UsuarioPublicoAPICall:

    def login(request):
        username = request.POST.get('email')
        password = request.POST.get('pass')
        data={'USUARIO': username, 'CONTRASENA': password}
        response = ApiCall.post('login',data,None)
        return response

    def recuperacionContrasena(request):
        email = request.POST.get('email')
        urlCambioPass = FRONT_ROUTE+'cambioclave'
        data ={
            "CORREO":email,
            "URL":urlCambioPass
        }
        response = ApiCall.post('recuperaciones-contrasenas',data,None)
        return response
    
    def validacionRecuperacionContrasena(request,pk):       
        clave = request.POST.get('clave1')
        data ={
            "CONTRASENA":clave
        }
        response = ApiCall.put_one('recuperaciones-contrasenas',pk,data)
        return response

class UsuariosAPICall:

    def get(request,query):
        header=currentheaders(request)
        usuarios='usuarios'
        r= ApiCall.get(usuarios,query,header)
        return r

    def post (request,data):
        r=ApiCall.post('usuarios',data,currentheaders(request))
        return r

    def put (request,data,pk):
        r=ApiCall.put('usuarios',data,pk,currentheaders(request))
        return r

class ProcesosAPICall:

    def get (request,query):
        r=ApiCall.get('procesos',query,currentheaders(request))
        return r
        
    def post (request,data):
        r=ApiCall.post('procesos',data,currentheaders(request))
        return r

    def put (request,data,pk):
        r=ApiCall.put('procesos',data,pk,currentheaders(request))
        return r

class SesionesAPICall:

    def get (request,query):
        r=ApiCall.get('sesiones',query,currentheaders(request))
        return r

    def post (request,data):
        r=ApiCall.post('sesiones',data,currentheaders(request))
        return r
    def put (request,data,pk):
        r=ApiCall.put('sesiones',data,pk,currentheaders(request))
        return r

class EstadosSesionesAPICall:
    def get (request,query):
        r=ApiCall.get('estados-sesiones',query,currentheaders(request))
        return r

class EstadosProcesosAPICall:
    def get (request,query):
        r=ApiCall.get('estados-procesos',query,currentheaders(request))
        return r


class ArchivosAPICall:
    def get (request,query):
        r=ApiCall.get('gestor-archivo',query,currentheaders(request))
        return r
    def post (request,data):
        r=ApiCall.post('gestor-archivo',data,currentheaders(request))
        return r

class EnlacesAPICall:
    def get (request,query):
        r=ApiCall.get('enlaces',query,currentheaders(request))
        return r
    def post (request,data):
        r=ApiCall.post('enlaces',data,currentheaders(request))
        return r