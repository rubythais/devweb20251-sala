from django.shortcuts import render
from django.views.generic import TemplateView,View
from adocato.forms import ContatoForm
from adocato.views.mixins import PerfilAdotanteMixin

class IndexView(TemplateView):
    """View para a página inicial do sistema."""
    
    template_name = "adocato/index.html"

class ContatoFormView(PerfilAdotanteMixin,View):

    template_name = "adocato/suporte/contato.html"

    form_class = ContatoForm

    def get(self, request, *args, **kwargs):
        """Exibe o formulário de contato."""
        form = self.form_class()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        """Processa o envio do formulário de contato."""
        form = self.form_class(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            mensagem = form.cleaned_data['mensagem']
            remetente = form.cleaned_data['remetente']
            return render(request, 'adocato/suporte/mensagem.html', {'mensagem': mensagem, 'titulo': titulo, 'remetente': remetente})
        return render(request, template_name=self.template_name, context={'form': form})
    


