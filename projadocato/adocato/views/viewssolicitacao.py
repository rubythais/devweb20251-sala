from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from adocato.utils import GerenciadorMensagens
from adocato.services.casousosolicitacao import CasoUsoSolicitacao
from adocato.services.casousodocumento import CasoUsoDocumento
from adocato.services.casousogato import CasoUsoGato
from adocato.services.casousoadotante import CasoUsoAdotante
from adocato.services.casousocoordenador import CasoUsoCoordenador
from adocato.views.mixins import PerfilAdotanteMixin, PerfilCoordenadorMixin
from adocato.models import Gato, Solicitacao, Avaliacao, Documento
from adocato.forms import AvaliacaoSolicitacaoForm, RecursoForm, DocumentoForm


class GatosDisponiveisView(ListView):
    """View para listar gatos disponíveis para adoção."""
    
    template_name = 'adocato/solicitacao/gatos_disponiveis.html'
    context_object_name = 'gatos'
    paginate_by = 6  # 6 gatos por página em formato de cards
    
    def get_queryset(self):
        """Retorna apenas gatos disponíveis."""
        return CasoUsoGato.buscar_gatos_disponiveis()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar parâmetros de filtro
        busca = self.request.GET.get('busca', '')
        if busca:
            context['busca'] = busca
            # Filtrar por busca se fornecida
            gatos = self.get_queryset().filter(nome__icontains=busca)
            context['object_list'] = gatos
        
        return context


class GatoDetalhesView(DetailView):
    """View para exibir detalhes de um gato disponível."""
    
    model = Gato
    template_name = 'adocato/solicitacao/gato_detalhes.html'
    context_object_name = 'gato'
    pk_url_kwarg = 'gato_id'
    
    def get_queryset(self):
        """Retorna apenas gatos disponíveis."""
        return CasoUsoGato.buscar_gatos()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gato = self.get_object()
        
        # Verificar se o usuário já tem solicitação para este gato
        if hasattr(self.request.user, 'id'):
            try:
                caso_uso = CasoUsoSolicitacao()
                solicitacao_existente = caso_uso.buscar_solicitacao_por_adotante_gato(
                    self.request.user.id, gato.id
                )
                if solicitacao_existente:
                    context['solicitacao_existente'] = solicitacao_existente
            except Exception:
                # Se não encontrar, não há problema
                pass
        
        return context


class IniciarSolicitacaoView(LoginRequiredMixin, PerfilAdotanteMixin, View):
    """View para iniciar uma nova solicitação de adoção."""
    
    def post(self, request, gato_id):
        try:
            # Verificar se o gato existe e está disponível via serviço de gatos
            gatos_disponiveis = CasoUsoGato.buscar_gatos_disponiveis()
            gato = None
            for g in gatos_disponiveis:
                if g.id == gato_id:
                    gato = g
                    break
            
            if not gato:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Gato não encontrado ou não disponível.")
                )
                return redirect('adocato:gatos_disponiveis')
            
            # Criar solicitação via serviço
            solicitacao = CasoUsoSolicitacao.criar_solicitacao(
                adotante_id=request.user.id,
                gato_id=gato_id
            )
            
            GerenciadorMensagens.processar_mensagem(
                request, 
                f"Solicitação de adoção para {gato.nome} criada com sucesso!"
            )
            
            return redirect('adocato:editar_solicitacao', solicitacao_id=solicitacao.id)
            
        except ValidationError as e:
            GerenciadorMensagens.processar_erros_validacao(request, e)
            return redirect('adocato:gato_detalhes', gato_id=gato_id)
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:gatos_disponiveis')


class EditarSolicitacaoView(LoginRequiredMixin, PerfilAdotanteMixin, View):
    """View para editar uma solicitação de adoção."""
    
    template_name = 'adocato/solicitacao/editar.html'
    
    def get(self, request, solicitacao_id):
        try:
            # Buscar a solicitação via serviço
            solicitacao = CasoUsoSolicitacao.buscar_solicitacao_com_relacionamentos(solicitacao_id)
            if not solicitacao or solicitacao.adotante_id != request.user.id:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Solicitação não encontrada.")
                )
                return redirect('adocato:minhas_solicitacoes')
            
            # Verificar se pode ser editada
            if solicitacao.status not in ['Em_Edicao', 'Reprovado']:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Esta solicitação não pode ser editada.")
                )
                return redirect('adocato:minhas_solicitacoes')
            
            # Buscar documentos via serviço
            documentos = CasoUsoDocumento.listar_documentos_solicitacao(solicitacao_id)
            
            context = {
                'solicitacao': solicitacao,
                'gato': solicitacao.gato,
                'pode_editar': True,
                'documentos': documentos,
                'documento_form': DocumentoForm()
            }
            
            return render(request, self.template_name, context)
            
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:minhas_solicitacoes')
    
    def post(self, request, solicitacao_id):
        try:
            # Buscar a solicitação via serviço
            solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
            if not solicitacao or solicitacao.adotante_id != request.user.id:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Solicitação não encontrada.")
                )
                return redirect('adocato:minhas_solicitacoes')
            
            # Verificar se pode ser editada
            if solicitacao.status not in ['Em_Edicao', 'Reprovado']:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Esta solicitação não pode ser editada.")
                )
                return redirect('adocato:minhas_solicitacoes')
            
            # Verificar se é upload de documento
            if 'acao' in request.POST and request.POST['acao'] == 'upload_documento':
                return self._processar_upload_documento(request, solicitacao)
            
            # Verificar se é remoção de documento
            if 'acao' in request.POST and request.POST['acao'] == 'remover_documento':
                return self._processar_remover_documento(request, solicitacao)
            
   
            
            # Enviar para avaliação se solicitado
            if 'acao' in request.POST and request.POST['acao'] == 'enviar':
                CasoUsoSolicitacao.enviar_solicitacao(solicitacao_id)
                GerenciadorMensagens.processar_mensagem(
                    request, 
                    "Solicitação enviada para avaliação com sucesso!"
                )
            else:
                GerenciadorMensagens.processar_mensagem(
                    request, 
                    "Solicitação atualizada com sucesso!"
                )
            
            return redirect('adocato:minhas_solicitacoes')
            
        except ValidationError as e:
            GerenciadorMensagens.processar_erros_validacao(request, e)
            return redirect('adocato:editar_solicitacao', solicitacao_id=solicitacao_id)
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:minhas_solicitacoes')
    
    def _processar_upload_documento(self, request, solicitacao):
        """Processa o upload de documentos."""
        try:
            # Para Django com múltiplos arquivos, vamos usar uma abordagem diferente
            arquivos = request.FILES.getlist('arquivo')
            if not arquivos:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Nenhum arquivo foi selecionado.")
                )
                return redirect('adocato:editar_solicitacao', solicitacao_id=solicitacao.id)
            
            documentos_criados = 0
            erros = []
            descricao_base = request.POST.get('descricao', '').strip()
            
            for i, arquivo in enumerate(arquivos):
                try:
                    # Validar arquivo individualmente
                    if not arquivo.name.lower().endswith(('.pdf', '.odt', '.docx')):
                        erros.append(f"{arquivo.name}: Formato não aceito. Use PDF, ODT ou DOCX.")
                        continue
                    
                    if arquivo.size > 10 * 1024 * 1024:  # 10MB
                        erros.append(f"{arquivo.name}: Arquivo muito grande (máximo 10MB).")
                        continue
                    
                    # Criar descrição
                    if descricao_base:
                        descricao = f"{descricao_base} - {arquivo.name}" if len(arquivos) > 1 else descricao_base
                    else:
                        descricao = f"Documento {i+1}: {arquivo.name}"
                    
                    # Criar documento via serviço
                    documento = CasoUsoDocumento.adicionar_documento(
                        solicitacao.id, arquivo, descricao
                    )
                    documentos_criados += 1
                
                except Exception as e:
                    erros.append(f"{arquivo.name}: {str(e)}")
            
            # Mensagens de resultado
            if documentos_criados > 0:
                mensagem = f"{documentos_criados} documento(s) enviado(s) com sucesso!"
                GerenciadorMensagens.processar_mensagem(request, mensagem)
            
            if erros:
                for erro in erros:
                    GerenciadorMensagens.processar_erros_validacao(
                        request, 
                        ValidationError(erro)
                    )
            
            return redirect('adocato:editar_solicitacao', solicitacao_id=solicitacao.id)
            
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:editar_solicitacao', solicitacao_id=solicitacao.id)
    
    def _processar_remover_documento(self, request, solicitacao):
        """Processa a remoção de um documento."""
        try:
            documento_id = request.POST.get('documento_id')
            if documento_id:
                # Buscar documento via serviço
                documento = CasoUsoDocumento.buscar_documento_por_id(documento_id)
                if documento and documento.solicitacao.id == solicitacao.id:
                    nome_arquivo = documento.arquivo.name
                    # Remover via serviço
                    CasoUsoDocumento.remover_documento(documento_id, request.user.id)
                    
                    GerenciadorMensagens.processar_mensagem(
                        request, 
                        f"Documento '{nome_arquivo}' removido com sucesso!"
                    )
                else:
                    GerenciadorMensagens.processar_erros_validacao(
                        request, 
                        ValidationError("Documento não encontrado.")
                    )
            
            return redirect('adocato:editar_solicitacao', solicitacao_id=solicitacao.id)
            
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:editar_solicitacao', solicitacao_id=solicitacao.id)


class MinhasSolicitacoesView(LoginRequiredMixin, PerfilAdotanteMixin, ListView):
    """View para listar solicitações do adotante."""
    
    template_name = 'adocato/solicitacao/minhas_solicitacoes.html'
    context_object_name = 'solicitacoes'
    paginate_by = 10
    
    def get_queryset(self):
        return CasoUsoSolicitacao.buscar_solicitacoes_adotante_com_relacionamentos(
            self.request.user.id
        )


class SolicitacaoDetalhesView(LoginRequiredMixin, PerfilAdotanteMixin, DetailView):
    """View para exibir detalhes de uma solicitação do adotante."""
    model = Solicitacao
    template_name = 'adocato/solicitacao/detalhes.html'
    context_object_name = 'solicitacao'
    pk_url_kwarg = 'solicitacao_id'
    
    def get_queryset(self):
        return CasoUsoSolicitacao.buscar_solicitacoes_adotante_com_relacionamentos(
            self.request.user.id
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitacao = self.get_object()
        
        # Buscar avaliações da solicitação via serviço
        context['avaliacoes'] = CasoUsoSolicitacao.get_avaliacoes_solicitacao(
            solicitacao.id
        )
        
        return context


class ImpetrarRecursoView(LoginRequiredMixin, PerfilAdotanteMixin, View):
    """View para impetrar recurso contra reprovação."""
    
    def post(self, request, solicitacao_id):
        try:
            # Buscar a solicitação via serviço
            solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
            if not solicitacao or solicitacao.adotante_id != request.user.id or solicitacao.status != 'Reprovada':
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Solicitação não encontrada ou não pode ter recurso impetrado.")
                )
                return redirect('adocato:minhas_solicitacoes')
            
            # Validar formulário
            form = RecursoForm(request.POST)
            if form.is_valid():
                motivo = form.cleaned_data['motivo']
                
                # Impetrar recurso via serviço
                CasoUsoSolicitacao.impetrar_recurso(solicitacao_id, motivo)
                
                GerenciadorMensagens.processar_mensagem(
                    request, 
                    "Recurso impetrado com sucesso! Sua solicitação será reavaliada."
                )
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        GerenciadorMensagens.processar_erros_validacao(
                            request, 
                            ValidationError(f"{field}: {error}")
                        )
            
            return redirect('adocato:minhas_solicitacoes')
            
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:minhas_solicitacoes')


class SolicitacoesPendentesView(LoginRequiredMixin, PerfilCoordenadorMixin, ListView):
    """View para coordenadores visualizarem solicitações pendentes."""
    
    template_name = 'adocato/solicitacao/pendentes.html'
    context_object_name = 'solicitacoes'
    paginate_by = 10
    
    def get_queryset(self):
        # Buscar parâmetros de filtro
        status_filtro = self.request.GET.get('status', 'Em_Analise')
        busca = self.request.GET.get('busca', '')
        
        filtros = {}
        if status_filtro and status_filtro != 'todos':
            filtros['status'] = status_filtro
        if busca:
            filtros['busca'] = busca
        
        return CasoUsoSolicitacao.buscar_solicitacoes_com_relacionamentos(filtros)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar filtros ao contexto
        context['status_filtro'] = self.request.GET.get('status', 'Pendente')
        context['busca'] = self.request.GET.get('busca', '')
        
        # Contar solicitações por status
        estatisticas=CasoUsoSolicitacao.estatisticas_solicitacoes()
        context['total_pendentes'] = estatisticas['em_analise']
        context['total_atrasadas'] = estatisticas['atrasadas']

        return context


class AvaliarSolicitacaoView(LoginRequiredMixin, PerfilCoordenadorMixin, View):
    """View para coordenadores avaliarem solicitações."""
    
    template_name = 'adocato/solicitacao/avaliar.html'
    
    def get(self, request, solicitacao_id):
        try:
            # Buscar a solicitação via serviço
            solicitacao = CasoUsoSolicitacao.buscar_solicitacao_com_relacionamentos(solicitacao_id)
            if not solicitacao:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Solicitação não encontrada.")
                )
                return redirect('adocato:solicitacoes_pendentes')
            
            # Verificar se pode ser avaliada
            if solicitacao.status != 'Em_Analise':
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Esta solicitação não está pendente de avaliação.")
                )
                return redirect('adocato:solicitacoes_pendentes')
            
            # Buscar avaliações anteriores via serviço
            avaliacoes_anteriores = CasoUsoSolicitacao.get_avaliacoes_solicitacao(solicitacao_id)
            
            # Buscar documentos da solicitação via serviço
            documentos = CasoUsoDocumento.listar_documentos_solicitacao(solicitacao_id)
            
            context = {
                'solicitacao': solicitacao,
                'form': AvaliacaoSolicitacaoForm(),
                'avaliacoes_anteriores': avaliacoes_anteriores[:5],  # Limitar a 5
                'documentos': documentos
            }
            
            return render(request, self.template_name, context)
            
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:solicitacoes_pendentes')
    
    def post(self, request, solicitacao_id):
        try:
            # Buscar a solicitação via serviço
            solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
            if not solicitacao:
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Solicitação não encontrada.")
                )
                return redirect('adocato:solicitacoes_pendentes')
            
            # Verificar se pode ser avaliada
            if solicitacao.status != 'Em_Analise':
                GerenciadorMensagens.processar_erros_validacao(
                    request, 
                    ValidationError("Esta solicitação não está pendente de avaliação.")
                )
                return redirect('adocato:solicitacoes_pendentes')
            
            # Validar formulário
            form = AvaliacaoSolicitacaoForm(request.POST)
            if form.is_valid():
                parecer = form.cleaned_data['parecer']
                decisao = form.cleaned_data['decisao']
                
                # Determinar status baseado na decisão
                novo_status = 'Aprovada' if decisao == 'aprovar' else 'Reprovada'
                
                # Avaliar solicitação via serviço
                CasoUsoSolicitacao.avaliar_solicitacao(
                    solicitacao_id=solicitacao_id,
                    coordenador_id=request.user.id,
                    parecer=parecer,
                    status=novo_status
                )
                
                mensagem = f"Solicitação {novo_status} com sucesso!"
                GerenciadorMensagens.processar_mensagem(request, mensagem)
                
                return redirect('adocato:solicitacoes_pendentes')
            else:
                # Reexibir formulário com erros usando serviço
                solicitacao = CasoUsoSolicitacao.buscar_solicitacao_com_relacionamentos(solicitacao_id)
                avaliacoes_anteriores = CasoUsoSolicitacao.get_avaliacoes_solicitacao(solicitacao_id)
                documentos = CasoUsoDocumento.listar_documentos_solicitacao(solicitacao_id)
                
                context = {
                    'solicitacao': solicitacao,
                    'form': form,
                    'avaliacoes_anteriores': avaliacoes_anteriores[:5],
                    'documentos': documentos
                }
                
                return render(request, self.template_name, context)
                
        except ValidationError as e:
            GerenciadorMensagens.processar_erros_validacao(request, e)
            return redirect('adocato:avaliar_solicitacao', solicitacao_id=solicitacao_id)
        except Exception as e:
            GerenciadorMensagens.processar_erros_validacao(request, ValidationError(str(e)))
            return redirect('adocato:solicitacoes_pendentes')
