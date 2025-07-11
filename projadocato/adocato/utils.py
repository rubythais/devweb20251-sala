from django.contrib import messages
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