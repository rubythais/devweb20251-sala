from django.urls import path
import adocato.views as views
from adocato.views.viewsgatos import (
    SalvarGatoView,
    ListarGatosView,
    ListarGatosDisponiveisView,
    ExcluirGatoView
)
from adocato.views.viewsracas import RacaListView
from adocato.views.viewsusuarios import (
    LoginView,
    LogoutView,
    PerfilUsuarioView
)
from adocato.views.viewsadotantes import (
    AdotanteRegistroView,
    AdotantePerfilEditView
)

from adocato.views.viewscoordenadores import (
    CoordenadorCadastroView,
    CoordenadorEditView,
    CoordenadorPerfilEditView,
    CoordenadorListView
)

from adocato.views.viewindex import (IndexView,ContatoFormView)

app_name = "adocato"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    
    # URLs dos Gatos
    path("gatos/listar", ListarGatosView.as_view(), name="listar_gatos"),
    path("gatos/salvar", SalvarGatoView.as_view(), name="cadastrar_gato"),
    path("gatos/salvar/<int:gato_id>/", SalvarGatoView.as_view(), name="atualizar_gato"),
    path("gatos/excluir/<int:gato_id>/", ExcluirGatoView.as_view(), name="excluir_gato"),
    path("gatos/disponiveis", ListarGatosDisponiveisView.as_view(), name="listar_gatos_disponiveis"),
    
    # URLs das Raças
    path("racas/listar", RacaListView.as_view(), name="listar_racas"),
    
    # URLs de Autenticação
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("perfil/", PerfilUsuarioView.as_view(), name="perfil"),

    #Urls de Contato
    path("suporte/contato/", ContatoFormView.as_view(), name="contato"),
    
    # URLs dos Adotantes
    path("adotante/registro/", AdotanteRegistroView.as_view(), name="cadastrar_adotante"),
    path("adotante/perfil/editar/", AdotantePerfilEditView.as_view(), name="atualizar_adotante"),
    
    # URLs dos Coordenadores
    path("coordenador/cadastro/", CoordenadorCadastroView.as_view(), name="cadastrar_coordenador"),
    path("coordenador/editar/<int:coordenador_id>/", CoordenadorEditView.as_view(), name="atualizar_coordenador"),
    path("coordenador/perfil/editar/", CoordenadorPerfilEditView.as_view(), name="atualizar_coordenador_perfil"),
    path("coordenador/listar/", CoordenadorListView.as_view(), name="listar_coordenadores"),
]