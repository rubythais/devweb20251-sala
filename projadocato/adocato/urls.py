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

from adocato.views.viewindex import IndexView

app_name = "adocato"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("gatos/listar", ListarGatosView.as_view(), name="listar_gatos"),
    path("gatos/salvar", SalvarGatoView.as_view(), name="cadastrar_gato"),
    path("gatos/salvar/<int:gato_id>/", SalvarGatoView.as_view(), name="atualizar_gato"),
    path("gatos/excluir/<int:gato_id>/", ExcluirGatoView.as_view(), name="excluir_gato"),
    path("gatos/disponiveis", ListarGatosDisponiveisView.as_view(), name="listar_gatos_disponiveis"),
    path("racas/listar", RacaListView.as_view(), name="listar_racas"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("perfil/", PerfilUsuarioView.as_view(), name="perfil"),
    # path("gatos/<int:gato
]