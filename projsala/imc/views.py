from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'index.html')

def soma(request):
    numero=2
    soma=numero+numero
    return HttpResponse(f'<h1>{numero} + {numero} = {soma}</h1>')

def calcular_imc(request):
    altura = float(request.GET.get('altura'))
    peso = float(request.GET.get('peso'))
    imc= peso/(altura*altura)
    if imc < 18.5:
        classificacao = 'Abaixo do peso'
    elif imc < 24.9:
        classificacao = 'Peso normal'
    elif imc < 29.9:
        classificacao = 'Sobrepeso'
    else:
        classificacao = 'Obesidade'
    contexto= {
        'imc': imc,
        'classificacao': classificacao,
        'altura': altura,
        'peso': peso,
    }
    return render(request, 'resultado_imc.html', contexto)