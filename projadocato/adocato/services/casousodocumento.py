from adocato.models import Documento, Solicitacao
from django.core.exceptions import ValidationError
from django.db import transaction


class CasoUsoDocumento:
    @staticmethod
    def listar_documentos_solicitacao(solicitacao_id):
        """Lista todos os documentos de uma solicitação."""
        return Documento.objects.filter(solicitacao_id=solicitacao_id).order_by('-enviado_em')
    
    @staticmethod
    def buscar_documento_por_id(documento_id):
        """Busca um documento pelo ID."""
        try:
            return Documento.objects.get(id=documento_id)
        except Documento.DoesNotExist:
            return None
    
    @staticmethod
    def adicionar_documento(solicitacao_id, arquivo, descricao=None):
        """
        Adiciona um documento à solicitação.
        Regras:
        - Apenas solicitações Em_Edicao ou Em_Recurso podem receber documentos
        """
        # Busca a solicitação
        try:
            solicitacao = Solicitacao.objects.get(id=solicitacao_id)
        except Solicitacao.DoesNotExist:
            raise ValidationError("Solicitação não encontrada.")
        
        # Verifica se a solicitação permite adição de documentos
        if solicitacao.status not in ['Em_Edicao', 'Em_Recurso']:
            raise ValidationError("Documentos só podem ser adicionados em solicitações em edição ou em recurso.")
        
        # Cria o documento
        documento = Documento(
            solicitacao=solicitacao,
            arquivo=arquivo,
            descricao=descricao or ""
        )
        
        try:
            documento.full_clean()
        except ValidationError as e:
            raise e
        
        documento.save()
        return documento
    
    @staticmethod
    def remover_documento(documento_id, usuario_id):
        """
        Remove um documento da solicitação.
        Regras:
        - Apenas o adotante da solicitação pode remover
        - Apenas quando solicitação está Em_Edicao ou Em_Recurso
        """
        documento = CasoUsoDocumento.buscar_documento_por_id(documento_id)
        if not documento:
            raise ValidationError("Documento não encontrado.")
        
        # Verifica se é o adotante da solicitação
        if documento.solicitacao.adotante.id != usuario_id:
            raise ValidationError("Apenas o adotante da solicitação pode remover documentos.")
        
        # Verifica se a solicitação permite remoção
        if documento.solicitacao.status not in ['Em_Edicao', 'Em_Recurso']:
            raise ValidationError("Documentos só podem ser removidos de solicitações em edição ou em recurso.")
        
        # Remove o arquivo do sistema de arquivos e o registro do banco
        if documento.arquivo:
            documento.arquivo.delete()
        
        documento.delete()
        return True
    
    @staticmethod
    def atualizar_descricao_documento(documento_id, nova_descricao, usuario_id):
        """
        Atualiza a descrição de um documento.
        Regras:
        - Apenas o adotante da solicitação pode atualizar
        - Apenas quando solicitação está Em_Edicao ou Em_Recurso
        """
        documento = CasoUsoDocumento.buscar_documento_por_id(documento_id)
        if not documento:
            raise ValidationError("Documento não encontrado.")
        
        # Verifica se é o adotante da solicitação
        if documento.solicitacao.adotante.id != usuario_id:
            raise ValidationError("Apenas o adotante da solicitação pode atualizar documentos.")
        
        # Verifica se a solicitação permite atualização
        if documento.solicitacao.status not in ['Em_Edicao', 'Em_Recurso']:
            raise ValidationError("Documentos só podem ser atualizados em solicitações em edição ou em recurso.")
        
        documento.descricao = nova_descricao or ""
        
        try:
            documento.full_clean()
        except ValidationError as e:
            raise e
        
        documento.save()
        return documento
    
    @staticmethod
    def pode_gerenciar_documento(documento_id, usuario_id):
        """
        Verifica se um usuário pode gerenciar (editar/remover) um documento.
        """
        documento = CasoUsoDocumento.buscar_documento_por_id(documento_id)
        if not documento:
            return False
        
        # Verifica se é o adotante da solicitação
        if documento.solicitacao.adotante.id != usuario_id:
            return False
        
        # Verifica se o status permite gerenciamento
        return documento.solicitacao.status in ['Em_Edicao', 'Em_Recurso']
