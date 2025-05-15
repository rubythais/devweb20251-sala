from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import services
# Create your views here.

def index(request):
    return render(request,'index.html')

def soma(request):
    numero=2
    soma=numero+numero
    return HttpResponse(f'<h1>{numero} + {numero} = {soma}</h1>')

def calcular_imc_view(request):
    if request.method == 'GET':
        return redirect('imc:index')
    altura = float(request.POST.get('altura'))
    peso = float(request.POST.get('peso'))
    imc_service=services.IMCService()
    contexto = imc_service.calcular_imc(altura, peso)
    return render(request, 'resultado_imc.html', contexto)