from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#definimos el login
def login(request):
    return render(request, 'login/login.html')
#definimos el menu
def menu(request):
    return render(request, 'menu/menu.html')
