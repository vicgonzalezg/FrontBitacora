from django.urls import path
from . import views 

urlpatterns = [
    path('', views.login),
    path('/', views.login),
    #path('menu/', views.menu),
    path('menuAdmin/', views.menuAdmin, name='menuAdmin'),
    path('procesosAdmin/', views.procesosAdmin, name='procesosAdmin'),
    path('nuevoProceso/', views.nuevoProceso, name='nuevoProceso'),
    path('modProceso/', views.modProceso, name='modProceso'),
    path('listProceso/', views.listProceso, name='listProceso'),
    path('termiProceso/', views.termiProceso, name='termiProceso'),
]