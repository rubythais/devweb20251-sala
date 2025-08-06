
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from adocato.utils import GerenciadorMensagens
from adocato.forms import (
    CoordenadorForm, CoordenadorPerfilForm
)
from adocato.services.casousocoordenador import CasoUsoCoordenador
from adocato.views.mixins import PerfilAdministradorMixin, PerfilCoordenadorMixin
class CoordenadorCadastroView(LoginRequiredMixin, PerfilAdministradorMixin, View):
    """View para cadastro de coordenadores (apenas superusuários)."""
    
    template_name = 'adocato/coordenador/form.html'
    
    def get(self, request):
        """Exibe o formulário de cadastro."""
        form = CoordenadorForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Processa o formulário de cadastro."""
        form = CoordenadorForm(request.POST)
        
        if form.is_valid():
            try:
                # Usa o serviço para cadastrar o coordenador
                coordenador = CasoUsoCoordenador.cadastrar_coordenador(
                    nome=form.cleaned_data['nome'],
                    cpf=form.cleaned_data['cpf'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data.get('email')
                )
                
                GerenciadorMensagens.processar_mensagem(
                    request, 
                    ValidationError(f"Coordenador {coordenador.nome} cadastrado com sucesso!")
                )
                return redirect('adocato:listar_coordenadores')
                
            except ValidationError as e:
                GerenciadorMensagens.processar_erros_validacao(request, e)
            except Exception as e:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError(f"Erro ao cadastrar coordenador: {str(e)}")
                )
        
        return render(request, self.template_name, {'form': form})


class CoordenadorEditView(LoginRequiredMixin, PerfilAdministradorMixin, View):
    """View para edição de coordenadores (apenas superusuários)."""
    
    template_name = 'adocato/coordenador/edit.html'
    
    def get(self, request, coordenador_id):
        """Exibe o formulário de edição."""
        coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(coordenador_id)
        
        if not coordenador:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError("Coordenador não encontrado."))
            return redirect('adocato:listar_coordenadores')
        
        # Preenche o formulário com os dados atuais
        initial_data = {
            'nome': coordenador.nome,
            'username': coordenador.username,
            'email': coordenador.email,
            'cpf': coordenador.cpf,
        }
        
        form = CoordenadorForm(initial=initial_data, is_edit=True)
        return render(request, self.template_name, {
            'form': form,
            'coordenador': coordenador
        })
    
    def post(self, request, coordenador_id):
        """Processa a edição do coordenador."""
        coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(coordenador_id)
        
        if not coordenador:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError("Coordenador não encontrado."))
            return redirect('adocato:listar_coordenadores')
        
        form = CoordenadorForm(request.POST, is_edit=True)
        
        if form.is_valid():
            try:
                # Atualiza o coordenador
                CasoUsoCoordenador.atualizar_coordenador(
                    coordenador_id=coordenador.id,
                    nome=form.cleaned_data['nome'],
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data.get('email'),
                    cpf=form.cleaned_data['cpf'],
                    password=form.cleaned_data.get('password') if form.cleaned_data.get('password') else None
                )

                GerenciadorMensagens.processar_mensagem(
                    request,
                    f"Coordenador {coordenador.nome} atualizado com sucesso!"
                )
                return redirect('adocato:listar_coordenadores')
                
            except ValidationError as e:
                GerenciadorMensagens.processar_erros_validacao(request, e)
            except Exception as e:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError(f"Erro ao atualizar coordenador: {str(e)}")
                )
        
        return render(request, self.template_name, {
            'form': form,
            'coordenador': coordenador
        })


class CoordenadorPerfilEditView(LoginRequiredMixin, PerfilCoordenadorMixin, View):
    """View para edição do próprio perfil do coordenador."""
    
    template_name = 'adocato/coordenador/perfil_edit.html'
    
    def get(self, request):
        """Exibe o formulário de edição do perfil."""
        coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(request.user.id)
        
        if not coordenador:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError("Coordenador não encontrado."))
            return redirect('adocato:index')
        
        # Preenche o formulário com os dados atuais
        initial_data = {
            'nome': coordenador.nome,
            'email': coordenador.email,
        }
        
        form = CoordenadorPerfilForm(initial=initial_data)
        return render(request, self.template_name, {
            'form': form,
            'coordenador': coordenador
        })
    
    def post(self, request):
        """Processa a edição do perfil."""
        coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(request.user.id)
        
        if not coordenador:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError("Coordenador não encontrado."))
            return redirect('adocato:index')
        
        form = CoordenadorPerfilForm(request.POST)
        
        if form.is_valid():
            try:
                # Atualiza apenas os campos do perfil
                CasoUsoCoordenador.atualizar_coordenador(
                    coordenador_id=coordenador.id,
                    nome=form.cleaned_data['nome'],
                    email=form.cleaned_data.get('email')
                )
                
                GerenciadorMensagens.processar_mensagem(
                    request, 
                    "Perfil atualizado com sucesso!"
                )
                return redirect('adocato:perfil')
                
            except ValidationError as e:
                GerenciadorMensagens.processar_erros_validacao(request, e)
            except Exception as e:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError(f"Erro ao atualizar perfil: {str(e)}")
                )
        
        return render(request, self.template_name, {
            'form': form,
            'coordenador': coordenador
        })


class CoordenadorListView(LoginRequiredMixin, PerfilAdministradorMixin, TemplateView):
    """View para listar coordenadores (apenas superusuários)."""
    
    template_name = 'adocato/coordenador/lista.html'
    
    def get_context_data(self, **kwargs):
        """Adiciona a lista de coordenadores ao contexto."""
        context = super().get_context_data(**kwargs)
        
        # Busca coordenadores com filtros opcionais
        nome = self.request.GET.get('nome')
        cpf = self.request.GET.get('cpf')
        username = self.request.GET.get('username')
        
        coordenadores = CasoUsoCoordenador.buscar_coordenadores(
            nome=nome,
            cpf=cpf,
            username=username
        )
        
        context['coordenadores'] = coordenadores
        context['filtros'] = {
            'nome': nome or '',
            'cpf': cpf or '',
            'username': username or '',
        }
        
        return context
