from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<h1> Bem-vindo(a) à aplicação IMC</h1>")

def soma(request):
    numero=2
    soma=numero+numero
    return HttpResponse(f'<h1>{numero} + {numero} = {soma}</h1>')