from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

#definimos el login
def login(request):
    if request.method == 'POST':
        admin={'nombre': 'María José','perfil':1}
        coach={'nombre': 'Nelson Gomez','perfil':2}
        coachee={'nombre': 'Victor Gonzalez','perfil':3}
        username = request.POST.get('user')
        password = request.POST.get('pass')
        print(username,password)
        if username == 'maria.jose' and password == 'inicio2021':
            return render(request,'menu/menuAdmin.html',{'usuario': admin})
        elif username== 'nelson.gomez' and password == 'inicio2021':
            return render(request,'menu/menuCoach.html',{'usuario': coach})
        elif username== 'victor.gonzalez' and password == 'inicio2021':
            return render(request,'menu/menuCoachee.html',{'usuario': coachee})
    return render(request, 'login/login.html')

#Menu
def menu(request):
    #if request.method == 'POST':
        #username = request.POST.get('user')
        #password = request.POST.get('pass')
        #print(username,password)
        #if username == 'maria.jose' and password == 'inicio2021':
        #    return render(request,'menu/menuAdmin.html')
        #elif username== 'juan.topo' and password == 'inicio2021':
        #    return render(request,'menu/menuCoach.html')

    return render(request, 'login/login.html')

#Paginas de Menu por Peril
def menuAdmin(request):
    return render(request,'menu/menuAdmin.html')

def menuCoach(request):
    return render(request,'menu/menuCoach.html')


def menuCoachee(request):
    return render(request,'menu/menuCoachee.html')

#Proceso
#def procesos(request):
#    return render(request, 'login/login.html')

#Paginas de Procesos
def procesosAdmin(request):
    return render(request,'procesos/procesosAdmin.html')