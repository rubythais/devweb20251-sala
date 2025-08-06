from .utils import GerenciadorSessaoUsuario


def usuario_context(request):
    """
    Context processor que adiciona informações do usuário em todos os templates.
    """
    return GerenciadorSessaoUsuario.determinar_tipo_usuario(request)
