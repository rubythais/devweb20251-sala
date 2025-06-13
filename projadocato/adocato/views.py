from django.shortcuts import render
from adocato.services.casousogato import CasoUsoGato
def index(request):
    return render(request, 'adocato/index.html')
def listar_gatos(request):
    """Lista todos os gatos disponíveis."""
    nome=request.GET.get('nome')
    if nome:
        gatos = CasoUsoGato.buscar_gatos_por_nome(nome)
    else:
        gatos = CasoUsoGato.listar_gatos()
    return render(request, 'adocato/gato/lista.html', {'gatos': gatos})