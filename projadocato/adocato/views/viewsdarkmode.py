from django.http import JsonResponse
from django.views import View

class ToogleDarkModeView(View):
    """View para alternar o modo escuro."""
    
    def get(self, request):
        """Alterna o modo escuro na sessão do usuário."""
        # Verifica se o modo escuro já está ativado
        if request.session.get('dark_mode', False):
            # Desativa o modo escuro
            request.session['dark_mode'] = False
        else:
            # Ativa o modo escuro
            request.session['dark_mode'] = True
        
        # Redireciona para a página anterior ou para a página inicial
        return JsonResponse({
            'dark_mode': request.session['dark_mode']
        })