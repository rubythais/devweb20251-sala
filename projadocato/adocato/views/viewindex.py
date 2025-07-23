from django.views.generic import TemplateView

class IndexView(TemplateView):
    """View para a página inicial do sistema."""
    
    template_name = "adocato/index.html"
    