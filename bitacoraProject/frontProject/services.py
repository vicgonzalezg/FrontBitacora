from . import models
import requests
import sys
import os
#Ordenar de A-Z
from . import models
from django.core import serializers
from django.apps import apps

class ValidRoute():
    def route(request):
        valid_route='127.0.0.1:8001'
        return valid_route
        
class  MantenedorArchivos():
    
    ValidRoute.route
    
class  MantenedorEnlaces():
    ValidRoute.route

class  MantenedorEstadoProcesos():
    ValidRoute.route

class  MantenedorEstadoSesiones():
    ValidRoute.route

class  MantenedorPerfiles():
    ValidRoute.route

class  MantenedorProcesos():
    ValidRoute.route

class  MantenedorSesiones():
    ValidRoute.route

class  MantenedorTipoArchivos():
    ValidRoute.route

class  MantenedorUsuarios():
    ValidRoute.route


class  LoginServices():
    def generate_request(params):
        response = requests.post(ValidRoute.route+'/login', params=params)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            return 'me tire'


