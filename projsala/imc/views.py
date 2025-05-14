from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'index.html')

def soma(request):
    numero=2
    soma=numero+numero
    return HttpResponse(f'<h1>{numero} + {numero} = {soma}</h1>')

def calcular_imc(request):
    if request.method == 'GET':
        return redirect('imc:index')
    altura = float(request.POST.get('altura'))
    peso = float(request.POST.get('peso'))
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