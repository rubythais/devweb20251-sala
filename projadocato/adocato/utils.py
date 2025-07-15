from django.contrib import messages


class GerenciadorSessaoUsuario:
    @staticmethod
    def determinar_tipo_usuario(request):
        """
        Determina o tipo de usuário (adotante ou coordenador) e armazena na sessão.
        Retorna um dicionário com informações do usuário.
        """
        if not request.user.is_authenticated:
            return {
                'tipo_usuario': 'anonimo',
                'eh_adotante': False,
                'eh_coordenador': False,
                'usuario_nome': None,
                'usuario_id': None
            }
        
        # Verifica se já existe na sessão e se é para o mesmo usuário
        sessao_key = f'tipo_usuario_{request.user.id}'
        if sessao_key in request.session:
            return request.session[sessao_key]
        
        # Importa aqui para evitar import circular
        from .services.casousoadotante import CasoUsoAdotante
        from .services.casousocoordenador import CasoUsoCoordenador
        
        # Verifica se é adotante
        adotante = CasoUsoAdotante.buscar_adotante_por_id(request.user.id)
        if adotante:
            info_usuario = {
                'tipo_usuario': 'adotante',
                'eh_adotante': True,
                'eh_coordenador': False,
                'usuario_nome': adotante.nome,
                'usuario_id': adotante.id,
                'usuario_email': adotante.email,
                'usuario_username': adotante.username
            }
        else:
            # Verifica se é coordenador
            coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(request.user.id)
            if coordenador:
                info_usuario = {
                    'tipo_usuario': 'coordenador',
                    'eh_adotante': False,
                    'eh_coordenador': True,
                    'usuario_nome': coordenador.nome,
                    'usuario_id': coordenador.id,
                    'usuario_email': coordenador.email,
                    'usuario_username': coordenador.username
                }
            else:
                # Usuário logado mas sem tipo específico
                info_usuario = {
                    'tipo_usuario': 'Administrador',
                    'eh_adotante': False,
                    'eh_coordenador': False,
                    'usuario_nome': request.user.username,
                    'usuario_id': request.user.id,
                    'usuario_email': request.user.email,
                    'usuario_username': request.user.username
                }
        
        # Armazena na sessão
        request.session[sessao_key] = info_usuario
        return info_usuario
    
    @staticmethod
    def limpar_sessao_usuario(request):
        """Remove as informações do usuário da sessão."""
        if request.user.is_authenticated:
            sessao_key = f'tipo_usuario_{request.user.id}'
            if sessao_key in request.session:
                del request.session[sessao_key]
    


class Utilitaria:
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """Formata o CPF para o padrão XXX.XXX.XXX-XX."""
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve conter 11 dígitos numéricos.")
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    @staticmethod
    def conversor_data(data):
        if isinstance(data, str) and data:
                try:
                    from datetime import datetime
                    data_obj = datetime.strptime(data, "%Y-%m-%d").date()
                except ValueError:
                    data_obj = data
        else:
            data_obj = data
        return data_obj
class GerenciadorMensagens():
    @staticmethod
    def processar_erros_validacao(request, validation_error):
        # Lista para armazenar mensagens únicas
        mensagens_unicas = set()
        
        if hasattr(validation_error, 'message_dict') and validation_error.message_dict:
            # Erros estruturados por campo
            for campo, erros in validation_error.message_dict.items():
                if isinstance(erros, list):
                    for erro in erros:
                        mensagem = f'{campo.title()}: {erro}'
                        mensagens_unicas.add(mensagem)
                else:
                    mensagem = f'{campo.title()}: {erros}'
                    mensagens_unicas.add(mensagem)
        elif hasattr(validation_error, 'messages') and validation_error.messages:
            # Lista de mensagens de erro
            for mensagem in validation_error.messages:
                mensagens_unicas.add(str(mensagem))
        else:
            # Mensagem simples
            mensagens_unicas.add(str(validation_error))
        
        # Adiciona apenas mensagens únicas
        for mensagem in mensagens_unicas:
            messages.error(request, mensagem)
    
    @staticmethod
    def processar_mensagem(request, mensagem):
        """Processa uma mensagem de sucesso ou informação."""
        if isinstance(mensagem, str):
            messages.success(request, mensagem)
        elif isinstance(mensagem, list):
            # Remove duplicatas da lista
            mensagens_unicas = list(set(mensagem))
            for msg in mensagens_unicas:
                messages.success(request, msg)
        else:
            raise ValueError("A mensagem deve ser uma string ou uma lista de strings.")