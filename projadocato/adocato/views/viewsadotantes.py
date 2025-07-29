from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from adocato.utils import GerenciadorMensagens, GerenciadorSessaoUsuario
from adocato.forms import (
    AdotanteForm, AdotantePerfilForm, 
)
from adocato.services.casousoadotante import CasoUsoAdotante
from adocato.views.mixins import  PerfilAdotanteMixin


class AdotanteRegistroView(View):
    """View para autocadastro de adotantes (usuários não logados)."""
    
    template_name = 'adocato/adotante/registro.html'
    
    def get(self, request):
        """Exibe o formulário de registro."""
        if request.user.is_authenticated:
            # Se já está logado, redireciona para o perfil
            return redirect('adocato:perfil')
        
        form = AdotanteForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Processa o formulário de registro."""
        if request.user.is_authenticated:
            return redirect('adocato:perfil')
        
        form = AdotanteForm(request.POST)
        
        if form.is_valid():
            try:
                # Usa o serviço para cadastrar o adotante
                adotante = CasoUsoAdotante.cadastrar_adotante(
                    nome=form.cleaned_data['nome'],
                    cpf=form.cleaned_data['cpf'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    data_nascimento=form.cleaned_data['data_nascimento'],
                    telefone=form.cleaned_data.get('telefone'),
                    cidade=form.cleaned_data.get('cidade'),
                    estado=form.cleaned_data.get('estado'),
                    email=form.cleaned_data.get('email')
                )
                
                # Autentica automaticamente o usuário após o cadastro
                user = authenticate(
                    request,
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                
                if user:
                    login(request, user)
                    GerenciadorSessaoUsuario.determinar_tipo_usuario(request)
                    GerenciadorMensagens.adicionar_sucesso(
                        request, 
                        f"Bem-vindo(a), {adotante.nome}! Seu cadastro foi realizado com sucesso."
                    )
                    return redirect('adocato:index')
                
            except ValidationError as e:
                GerenciadorMensagens.processar_erros_validacao(request, e)
            except Exception as e:
                GerenciadorMensagens.adicionar_erro(
                    request, 
                    f"Erro ao cadastrar adotante: {str(e)}"
                )
        
        return render(request, self.template_name, {'form': form})


class AdotantePerfilEditView(LoginRequiredMixin, PerfilAdotanteMixin, View):
    """View para edição do perfil do adotante."""
    
    template_name = 'adocato/adotante/perfil_edit.html'
    
    def get(self, request):
        """Exibe o formulário de edição do perfil."""
        adotante = CasoUsoAdotante.buscar_adotante_por_id(request.user.id)
        
        if not adotante:
            GerenciadorMensagens.adicionar_erro(request, "Adotante não encontrado.")
            return redirect('adocato:index')
        
        # Preenche o formulário com os dados atuais
        initial_data = {
            'nome': adotante.nome,
            'email': adotante.email,
            'telefone': adotante.telefone,
            'cidade': adotante.cidade,
            'estado': adotante.estado,
        }
        
        form = AdotantePerfilForm(initial=initial_data)
        return render(request, self.template_name, {
            'form': form,
            'adotante': adotante
        })
    
    def post(self, request):
        """Processa a edição do perfil."""
        adotante = CasoUsoAdotante.buscar_adotante_por_id(request.user.id)
        
        if not adotante:
            GerenciadorMensagens.adicionar_erro(request, "Adotante não encontrado.")
            return redirect('adocato:index')
        
        form = AdotantePerfilForm(request.POST)
        
        if form.is_valid():
            try:
                # Atualiza apenas os campos do perfil
                CasoUsoAdotante.atualizar_adotante(
                    adotante_id=adotante.id,
                    nome=form.cleaned_data['nome'],
                    telefone=form.cleaned_data.get('telefone'),
                    cidade=form.cleaned_data.get('cidade'),
                    estado=form.cleaned_data.get('estado'),
                    email=form.cleaned_data.get('email')
                )
                
                GerenciadorMensagens.adicionar_sucesso(
                    request, 
                    "Perfil atualizado com sucesso!"
                )
                return redirect('adocato:perfil')
                
            except ValidationError as e:
                GerenciadorMensagens.processar_erros_validacao(request, e)
            except Exception as e:
                GerenciadorMensagens.adicionar_erro(
                    request, 
                    f"Erro ao atualizar perfil: {str(e)}"
                )
        
        return render(request, self.template_name, {
            'form': form,
            'adotante': adotante
        })

