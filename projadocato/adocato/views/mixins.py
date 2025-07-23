from adocato.services.casousocoordenador import CasoUsoCoordenador
from adocato.services.casousoadotante import CasoUsoAdotante
from django.contrib.auth.mixins import UserPassesTestMixin
from adocato.utils import GerenciadorMensagens  # Adicione o import correto aqui
from django.core.exceptions import ValidationError

"""
Classes Mixins permitem definir blocos de código que podem ser reutilizados em diferentes views,
sem a necessidade de herdar de uma classe base específica. Elas são úteis para compartilhar funcionalidades comuns
entre diferentes views, como verificações de permissão, manipulação de contexto, etc.
No Django, Mixins são frequentemente usados com class-based views (CBVs) para adicionar funcionalidades
específicas sem precisar criar uma hierarquia complexa de classes.
Conceito geral de Mixins https://docs.djangoproject.com/en/5.2/topics/class-based-views/mixins/

Tutorial geral: https://docs.djangoproject.com/en/5.2/topics/class-based-views/mixins/

"""

class PerfilCoordenadorMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário é um coordenador."""
    #raise_exception=True #Nesse caso o mixin acaba oferecendo mais recursos do que o user_passes_test
    def test_func(self):
        coordenador = CasoUsoCoordenador.buscar_coordenador_por_id(self.request.user.id)
        if not coordenador:
            GerenciadorMensagens.processar_erros_validacao(self.request, ValidationError("Você não é um coordenador."))
            # O mixin já redireciona para a página de login com uma mensagem de
        #Como aqui você tem acesso ao request, você poderia registrar uma mensagem de erro como:
        #GerenciadorMensagens.processar_erros_validacao(self.request, ValidationError("Você não é um coordenador."))
     
        return coordenador is not None
class PerfilAdotanteMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário é um adotante."""
    raise_exception=True #Nesse caso o mixin acaba oferecendo mais recursos do que o user_passes_test
    def test_func(self):
        adotante = CasoUsoAdotante.buscar_adotante_por_id(self.request.user.id)
        return adotante is not None

class PerfilAdministradorMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário é um administrador."""
    raise_exception=True #Nesse caso o mixin acaba oferecendo mais recursos do que o user_passes_test
    def test_func(self):
        return self.request.user.is_superuser