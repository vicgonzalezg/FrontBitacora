from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

#definimos el login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')
        print(username,password)
        if username == 'maria.jose' and password == 'inicio2021':
            return render(request,'menu/menuAdmin.html')
        elif username== 'nelson.gomez' and password == 'inicio2021':
            return render(request,'menu/menuCoach.html')
        elif username== 'victor.gonzalez' and password == 'inicio2021':
            return render(request,'menu/menuCoachee.html')
    return render(request, 'login/login.html')

#definimos el menu
def menu(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')
        print(username,password)
        if username == 'maria.jose' and password == 'inicio2021':
            return render(request,'menu/menuAdmin.html')
        elif username== 'juan.topo' and password == 'inicio2021':
            return render(request,'menu/menuCoach.html')

    return render(request, 'login/login.html')


def menuAdmin(request):
    return render(request,'menu/menuAdmin.html')

def menuCoach(request):
    return render(request,'menu/menuCoach.html')


def menuCoachee(request):
    return render(request,'menu/menuCoachee.html')

