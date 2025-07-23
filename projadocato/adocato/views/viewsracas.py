from adocato.views.mixins import PerfilCoordenadorMixin
from adocato.services.casousoraca import CasoUsoRaca
from django.views.generic import ListView

class RacaListView(PerfilCoordenadorMixin, ListView):
    """View para listar as raças de gatos."""
    
    template_name = 'adocato/raca/lista.html'
    context_object_name = 'racas'
    
    def get_queryset(self):
        raca_nome = self.request.GET.get('raca')
        """Retorna todas as raças de gatos."""
        return CasoUsoRaca.buscar_racas(nome=raca_nome)