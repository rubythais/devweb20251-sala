from adocato.models import Solicitacao, Gato, Adotante, Coordenador, Avaliacao
from django.core.exceptions import ValidationError
from django.db import transaction


class CasoUsoSolicitacao:
    @staticmethod
    def listar_solicitacoes():
        """Lista todas as solicitações cadastradas no banco de dados."""
        return Solicitacao.objects.all()
    
    @staticmethod
    def buscar_solicitacao_por_id(solicitacao_id):
        """Busca uma solicitação pelo ID."""
        try:
            return Solicitacao.objects.get(id=solicitacao_id)
        except Solicitacao.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_solicitacao_com_relacionamentos(solicitacao_id):
        """Busca uma solicitação com relacionamentos carregados."""
        try:
            return Solicitacao.objects.select_related(
                'gato', 'gato__raca', 'adotante'
            ).get(id=solicitacao_id)
        except Solicitacao.DoesNotExist:
            return None
    
    @staticmethod
    def buscar_solicitacoes(adotante_id=None, gato_id=None, status=None):
        """Busca solicitações com filtros opcionais: adotante, gato ou status."""
        query = Solicitacao.objects.all()
        
        if adotante_id:
            query = query.filter(adotante_id=adotante_id)
        if gato_id:
            query = query.filter(gato_id=gato_id)
        if status:
            query = query.filter(status=status)
        
        return query
    
    @staticmethod
    def buscar_solicitacoes_com_relacionamentos(filtros=None):
        """Busca solicitações com relacionamentos carregados."""
        query = Solicitacao.objects.select_related('gato', 'gato__raca', 'adotante')
        
        if filtros:
            if 'status' in filtros and filtros['status'] != 'todos':
                query = query.filter(status=filtros['status'])
            if 'busca' in filtros and filtros['busca']:
                busca = filtros['busca']
                query = query.filter(
                    gato__nome__icontains=busca
                ) | query.filter(
                    adotante__nome__icontains=busca
                )
        
        return query.order_by('dataSolicitacao')
    
    @staticmethod
    def buscar_solicitacoes_adotante_com_relacionamentos(adotante_id):
        """Busca solicitações de um adotante com relacionamentos carregados."""
        return Solicitacao.objects.filter(
            adotante_id=adotante_id
        ).select_related('gato', 'gato__raca').order_by('-dataSolicitacao')
    
    @staticmethod
    def buscar_solicitacoes_por_adotante(adotante_id):
        """Busca todas as solicitações de um adotante específico."""
        return Solicitacao.objects.filter(adotante_id=adotante_id)
    
    @staticmethod
    def buscar_solicitacao_por_adotante_gato(adotante_id, gato_id):
        """Busca solicitação específica de um adotante para um gato."""
        return Solicitacao.objects.filter(
            adotante_id=adotante_id, 
            gato_id=gato_id
        ).first()
    
    @staticmethod
    def buscar_solicitacoes_por_coordenador(coordenador_id):
        """Busca todas as solicitações que um coordenador pode avaliar."""
        return Solicitacao.objects.filter(status__in=['Em_Analise'])
    
    @staticmethod
    @transaction.atomic
    def criar_solicitacao(adotante_id, gato_id):
        """
        Cria uma nova solicitação.
        Regras:
        - O gato deve estar disponível
        - O gato fica indisponível quando a solicitação é criada
        - Status inicial: Em_Edicao
        """
        # Busca o adotante
        try:
            adotante = Adotante.objects.get(id=adotante_id)
        except Adotante.DoesNotExist:
            raise ValidationError("Adotante não encontrado.")
        
        # Busca o gato
        try:
            gato = Gato.objects.get(id=gato_id)
        except Gato.DoesNotExist:
            raise ValidationError("Gato não encontrado.")
        
        # Verifica se o gato está disponível
        if not gato.disponivel:
            raise ValidationError("Este gato não está disponível para adoção.")
        
        # Verifica se já existe uma solicitação ativa para este gato
        solicitacao_existente = Solicitacao.objects.filter(
            gato=gato,
            status__in=['Em_Edicao', 'Em_Analise', 'Em_Recurso']
        ).first()
        
        if solicitacao_existente:
            raise ValidationError("Já existe uma solicitação ativa para este gato.")
        
        # Cria a solicitação
        solicitacao = Solicitacao(
            adotante=adotante,
            gato=gato,
            status='Em_Edicao'
        )
        
        try:
            solicitacao.full_clean()
        except ValidationError as e:
            raise e
        
        # Salva a solicitação e torna o gato indisponível
        solicitacao.save()
        gato.disponivel = False
        gato.save()
        
        return solicitacao
    
    @staticmethod
    def enviar_solicitacao(solicitacao_id):
        """
        Envia a solicitação para análise.
        Regras:
        - Apenas solicitações Em_Edicao podem ser enviadas
        - Muda status para Em_Analise
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            raise ValidationError("Solicitação não encontrada.")
        
        if solicitacao.status != 'Em_Edicao':
            raise ValidationError("Apenas solicitações em edição podem ser enviadas para análise.")
        
        solicitacao.status = 'Em_Analise'
        try:
            solicitacao.full_clean()
        except ValidationError as e:
            raise e
        
        solicitacao.save()
        return solicitacao
    
    @staticmethod
    @transaction.atomic
    def avaliar_solicitacao(solicitacao_id, coordenador_id, parecer, status):
        """
        Coordenador avalia uma solicitação.
        Regras:
        - Apenas solicitações Pendente podem ser avaliadas
        - Se aprovada: status = Aprovado
        - Se reprovada: status = Reprovado (gato volta a ficar disponível)
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            raise ValidationError("Solicitação não encontrada.")
        
        if solicitacao.status != 'Em_Analise':
            raise ValidationError("Apenas solicitações pendentes podem ser avaliadas.")
        
        # Busca o coordenador
        try:
            coordenador = Coordenador.objects.get(id=coordenador_id)
        except Coordenador.DoesNotExist:
            raise ValidationError("Coordenador não encontrado.")
        
        
        # Cria a avaliação
        avaliacao = Avaliacao(
            solicitacao=solicitacao,
            coordenador=coordenador,
            parecer=parecer
        )
        
        try:
            avaliacao.full_clean()
        except ValidationError as e:
            raise e
        
        avaliacao.save()
        
        # Atualiza o status da solicitação
        if status == 'Aprovada':
            solicitacao.status = 'Aprovada'
        else:
            solicitacao.status = 'Reprovada'
            # Se reprovada, gato volta a ficar disponível
            solicitacao.gato.disponivel = True
            solicitacao.gato.save()
        
        solicitacao.save()
        return solicitacao, avaliacao
    @transaction.atomic
    @staticmethod
    def impetrar_recurso(solicitacao_id, motivo_recurso):
        """
        Adotante impetra recurso contra solicitação reprovada.
        Regras:
        - Apenas solicitações Reprovado podem ter recurso
        - Apenas um recurso por solicitação
        - Status muda para Em_Recurso
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            raise ValidationError("Solicitação não encontrada.")
        
        if solicitacao.status != 'Reprovada':
            raise ValidationError("Apenas solicitações reprovadas podem ter recurso impetrado.")
        
        # Verifica se já houve recurso
        if solicitacao.recurso:
            raise ValidationError("Esta solicitação já teve um recurso impetrado.")
        
        if not motivo_recurso or len(motivo_recurso.strip()) < 10:
            raise ValidationError("O motivo do recurso deve ter pelo menos 10 caracteres.")
        
        solicitacao.recurso = motivo_recurso
        solicitacao.status = 'Em_Recurso'
        solicitacao.gato.disponivel = False  # Gato fica indisponível durante o recurso
        
        try:
            solicitacao.full_clean()
        except ValidationError as e:
            raise e
        
        solicitacao.save()
        solicitacao.gato.save()
        return solicitacao
    
    @staticmethod
    def enviar_recurso(solicitacao_id):
        """
        Envia recurso para nova análise.
        Regras:
        - Apenas solicitações Em_Recurso podem ser enviadas
        - Status volta para Em_Analise
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            raise ValidationError("Solicitação não encontrada.")
        
        if solicitacao.status != 'Em_Recurso':
            raise ValidationError("Apenas solicitações em recurso podem ser enviadas para nova análise.")
        
        if not solicitacao.recurso or len(solicitacao.recurso.strip()) < 10:
            raise ValidationError("É necessário informar o motivo do recurso antes de enviar.")
        
        solicitacao.status = 'Em_Analise'
        solicitacao.save()
        return solicitacao
    
    @staticmethod
    def atualizar_recurso(solicitacao_id, motivo_recurso):
        """
        Atualiza o motivo do recurso.
        Regras:
        - Apenas solicitações Em_Recurso podem ter recurso atualizado
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            raise ValidationError("Solicitação não encontrada.")
        
        if solicitacao.status != 'Em_Recurso':
            raise ValidationError("Apenas solicitações em recurso podem ter o motivo alterado.")
        
        if not motivo_recurso or len(motivo_recurso.strip()) < 10:
            raise ValidationError("O motivo do recurso deve ter pelo menos 10 caracteres.")
        
        solicitacao.recurso = motivo_recurso
        solicitacao.save()
        return solicitacao
    
    @staticmethod
    @transaction.atomic
    def cancelar_solicitacao(solicitacao_id):
        """
        Cancela uma solicitação.
        Regras:
        - Apenas solicitações Em_Edicao ou Em_Recurso podem ser canceladas
        - O gato volta a ficar disponível
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            raise ValidationError("Solicitação não encontrada.")
        
        if solicitacao.status not in ['Em_Edicao', 'Em_Recurso']:
            raise ValidationError("Apenas solicitações em edição ou em recurso podem ser canceladas.")
        
        # Torna o gato disponível novamente
        solicitacao.gato.disponivel = True
        solicitacao.gato.save()
        
        # Remove a solicitação
        solicitacao.delete()
        return True
    
    @staticmethod
    def pode_editar_solicitacao(solicitacao_id, usuario_id):
        """
        Verifica se um usuário pode editar uma solicitação.
        Regras:
        - Apenas o adotante proprietário pode editar
        - Apenas quando status = Em_Edicao ou Em_Recurso
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            return False
        
        # Verifica se é o adotante da solicitação
        if solicitacao.adotante.id != usuario_id:
            return False
        
        # Verifica se o status permite edição
        return solicitacao.status in ['Em_Edicao', 'Em_Recurso']
    
    @staticmethod
    def pode_avaliar_solicitacao(solicitacao_id, coordenador_id):
        """
        Verifica se um coordenador pode avaliar uma solicitação.
        Regras:
        - Apenas coordenadores podem avaliar
        - Apenas quando status = Em_Analise
        - Coordenador não pode ter avaliado anteriormente
        """
        solicitacao = CasoUsoSolicitacao.buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao:
            return False
        
        if solicitacao.status != 'Em_Analise':
            return False
        
        # Verifica se o coordenador já avaliou
        avaliacao_existente = Avaliacao.objects.filter(
            solicitacao=solicitacao,
            coordenador_id=coordenador_id
        ).exists()
        
        return not avaliacao_existente
    
    @staticmethod
    def get_avaliacoes_solicitacao(solicitacao_id):
        """Retorna todas as avaliações de uma solicitação."""
        return Avaliacao.objects.filter(solicitacao_id=solicitacao_id).order_by('-dataAvaliacao')
    
    @staticmethod
    def buscar_solicitacoes_atrasadas():
        """Busca solicitações que estão atrasadas (mais de 7 dias em análise ou recurso)."""
        solicitacoes = Solicitacao.objects.filter(
            status__in=['Em_Analise', 'Em_Recurso']
        )
        return [s for s in solicitacoes if s.esta_atrasado()]
    
    @staticmethod
    def get_estatisticas():
        """Retorna estatísticas gerais das solicitações."""
        total = Solicitacao.objects.count()
        em_edicao = Solicitacao.objects.filter(status='Em_Edicao').count()
        em_analise = Solicitacao.objects.filter(status='Em_Analise').count()
        aprovadas = Solicitacao.objects.filter(status='Aprovada').count()
        reprovadas = Solicitacao.objects.filter(status='Reprovada').count()
        em_recurso = Solicitacao.objects.filter(status='Em_Recurso').count()
        
        return {
            'total': total,
            'em_edicao': em_edicao,
            'em_analise': em_analise,
            'aprovadas': aprovadas,
            'reprovadas': reprovadas,
            'em_recurso': em_recurso,
            'atrasadas': len(CasoUsoSolicitacao.buscar_solicitacoes_atrasadas())
        }
    
    @staticmethod
    def estatisticas_solicitacoes():
        """Alias para get_estatisticas para compatibilidade."""
        return CasoUsoSolicitacao.get_estatisticas()
