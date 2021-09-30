from django.urls import path
from . import views 

urlpatterns = [
    path('', views.login),
    #path('/', views.login),
    #path('menu/', views.menu),
    path('menuAdmin/', views.menuAdmin, name='menuAdmin'),
    path('procesosAdmin/', views.procesosAdmin, name='procesosAdmin'),
    path('nuevoProceso/', views.nuevoProceso, name='nuevoProceso'),
    path('buscaProceso/', views.buscaProceso, name='buscaProceso'),
    path('modProceso/', views.modProceso, name='modProceso'),
    path('listProceso/', views.listProceso, name='listProceso'),
    path('termiProceso/', views.termiProceso, name='termiProceso'),
    path('infoProceso/', views.infoProceso, name='infoProceso'),
    path('usuariosAdmin/', views.usuariosAdmin, name='usuariosAdmin'),
    path('nuevoUsuario/', views.nuevoUsuario, name='nuevoUsuario'),
    path('modUsuario/', views.modUsuario, name='modUsuario'),
    path('listUsuarios/', views.listUsuarios, name='listUsuarios'),
    path('estadoUsuarios/', views.estadoUsuarios, name='estadoUsuarios'),

    #Perteneciente al proceso de Coach
    path('menuCoach/', views.menuCoach, name='menuCoach'),
    path('listProCoach/', views.listProCoach, name='listProCoach'),
    path('procAsig/', views.procAsig, name='procAsig'),

    #Perteneciente al proceso de Coachee
    path('menuCoachee/', views.menuCoachee, name='menuCoachee'),
    path('infoProCoachee/', views.infoProCoachee, name='infoProCoachee'),
]