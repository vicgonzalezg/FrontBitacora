from django.urls import path
from . import views 

urlpatterns = [
    path('', views.login),
    path('/', views.login),
    #path('menu/', views.menu),
    path('menuAdmin/', views.menuAdmin, name='menuAdmin'),
    path('procesosAdmin/', views.procesosAdmin, name='procesosAdmin'),
    path('nuevoProceso/', views.nuevoProceso, name='nuevoProceso'),

]