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
from adocato.views.viewssolicitacao import (
    GatosDisponiveisView,
    GatoDetalhesView,
    IniciarSolicitacaoView,
    EditarSolicitacaoView,
    MinhasSolicitacoesView,
    SolicitacaoDetalhesView,
    ImpetrarRecursoView,
    SolicitacoesPendentesView,
    AvaliarSolicitacaoView
)

from adocato.views.viewsdarkmode import ToogleDarkModeView

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
    
    # URLs das Solicitações de Adoção
    path("solicitacao/gatos/", GatosDisponiveisView.as_view(), name="gatos_disponiveis"),
    path("solicitacao/gato/<int:gato_id>/", GatoDetalhesView.as_view(), name="gato_detalhes"),
    path("solicitacao/iniciar/<int:gato_id>/", IniciarSolicitacaoView.as_view(), name="iniciar_solicitacao"),
    path("solicitacao/editar/<int:solicitacao_id>/", EditarSolicitacaoView.as_view(), name="editar_solicitacao"),
    path("solicitacao/minhas/", MinhasSolicitacoesView.as_view(), name="minhas_solicitacoes"),
    path("solicitacao/detalhes/<int:solicitacao_id>/", SolicitacaoDetalhesView.as_view(), name="solicitacao_detalhes"),
    path("solicitacao/recurso/<int:solicitacao_id>/", ImpetrarRecursoView.as_view(), name="impetrar_recurso"),
    
    # URLs para Coordenadores - Avaliação de Solicitações
    path("coordenador/solicitacoes/pendentes/", SolicitacoesPendentesView.as_view(), name="solicitacoes_pendentes"),
    path("coordenador/solicitacao/avaliar/<int:solicitacao_id>/", AvaliarSolicitacaoView.as_view(), name="avaliar_solicitacao"),

    #URls para alternar o modo escuro
    path("toogle-dark-mode/", ToogleDarkModeView.as_view(), name="toogle_dark_mode"),
]