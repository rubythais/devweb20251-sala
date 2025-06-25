from django.shortcuts import render
from .services import LeilaoService
# Create your views here.

def index(request):
    leiloes=LeilaoService.listar_leiloes()
    contexto={'leiloes':leiloes}
    return render(request, 'leilao/index.html',context=contexto)