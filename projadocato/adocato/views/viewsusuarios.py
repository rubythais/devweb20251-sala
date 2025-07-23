from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from adocato.utils import GerenciadorMensagens, GerenciadorSessaoUsuario


class LoginView(View):
    """View para login de usuários."""
    
    def get(self, request):
        """Exibe o formulário de login."""
        return render(request, 'adocato/login.html')
    
    def post(self, request):
        """Processa o formulário de login."""
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Força a determinação do tipo de usuário na sessão
            GerenciadorSessaoUsuario.determinar_tipo_usuario(request)
            return redirect('adocato:index')
        else:
            GerenciadorMensagens.processar_erros_validacao(
                request, 
                ValidationError("Usuário ou senha inválidos.")
            )
            return render(request, 'adocato/login.html')


class LogoutView(LoginRequiredMixin, View):
    """View para logout de usuários."""
    
    def get(self, request):
        """Processa o logout do usuário."""
        return self.logout_user(request)
    
    def post(self, request):
        """Processa o logout do usuário."""
        return self.logout_user(request)
    
    def logout_user(self, request):
        """Método comum para logout."""
        # Limpa as informações da sessão antes do logout
        GerenciadorSessaoUsuario.limpar_sessao_usuario(request)
        logout(request)
        return redirect('adocato:login')


class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    """View para exibir o perfil do usuário."""
    
    template_name = 'adocato/perfil.html'
    
    def get_context_data(self, **kwargs):
        """
        Adiciona informações do usuário ao contexto.
        As informações do usuário estão automaticamente disponíveis no template
        através do context processor.
        """
        context = super().get_context_data(**kwargs)
        # Pode adicionar contexto adicional aqui se necessário
        return context
