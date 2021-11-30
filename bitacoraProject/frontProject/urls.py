from django.urls import path
from . import views 

urlpatterns = [
    path('', views.login),
    path('logout/', views.logout, name='logout'),
    path('recuperarClave/', views.recuperarClave, name='recuperarClave'),
    path('cambioclave/<str:pk>', views.cambioclave, name='cambioclave'),
    #path('menu/', views.menu),
    path('menuAdmin/', views.menuAdmin, name='menuAdmin'),
    path('procesosAdmin/', views.procesosAdmin, name='procesosAdmin'),
    path('nuevoProceso/', views.nuevoProceso, name='nuevoProceso'),
    path('buscaProceso/', views.buscaProceso, name='buscaProceso'),
    path('modProceso/<int:id>/', views.modProceso, name='modProceso'),
    path('visInfoProceso/<int:id>/', views.visInfoProceso, name='visInfoProceso'),
    path('finProceso/<int:id>/', views.finProceso, name='finProceso'),
    path('usuariosAdmin/', views.usuariosAdmin, name='usuariosAdmin'),
    path('nuevoUsuario/', views.nuevoUsuario, name='nuevoUsuario'),
    path('listUsuarios/', views.listUsuarios, name='listUsuarios'),
    path('modUsuarios/<int:id>/', views.modUsuarios, name='modUsuarios'),
    #path('buscaUsuarios/', views.buscaUsuarios, name='buscaUsuarios'),
    #para enlaces y archivos
    #path('infoSesionCoachDocument/<int:id>/', views.infoSesionCoachDocument, name='infoSesionCoachDocument'),


    #Perfil de usuario
    path('perfil/', views.perfil, name='perfil'),

    #Perteneciente al proceso de Coach
    path('menuCoach/', views.menuCoach, name='menuCoach'),
    path('listProCoach/', views.listProCoach, name='listProCoach'),
    path('procAsig/', views.procAsig, name='procAsig'),
    path('infoProCoach/<int:id>/', views.infoProCoach, name='infoProCoach'),
    path('infoSesionCoach/<int:id>/', views.infoSesionCoach, name='infoSesionCoach'),
    path('infoEnlaceSesionCoach/<int:id>/', views.infoEnlaceSesionCoach, name='infoEnlaceSesionCoach'),

    #Perteneciente al proceso de Coachee
    path('menuCoachee/', views.menuCoachee, name='menuCoachee'),
    path('infoProCoachee/<int:id>/', views.infoProCoachee, name='infoProCoachee'),
    path('modPlanAccion/<int:id>/', views.modPlanAccion, name='modPlanAccion'),
    path('modSesionAvance/<int:id>/', views.modSesionAvance, name='modSesionAvance'),
    path('imprimirProceso/<int:id>/', views.imprimirProceso, name='imprimirProceso'),
]