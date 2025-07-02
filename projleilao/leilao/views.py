from django.shortcuts import render
from .services import LeilaoService
# Create your views here.

def index(request):
    leiloes=LeilaoService.listar_leiloes()
    contexto={'leiloes':leiloes}
    return render(request, 'leilao/index.html',context=contexto)
def listar_itensLeilao(request,leilao_id):
    titulo=request.GET.get('titulo',None)
    itensLeilao=LeilaoService.listar_itensLeilao(leilao_id,titulo)
    contexto={'itensLeilao':itensLeilao,'leilao_id':leilao_id}
    return render(request, 'leilao/itens.html',context=contexto)