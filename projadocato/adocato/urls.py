from django.urls import path
import adocato.views as views
app_name = "adocato"
urlpatterns = [
    path("", views.index, name="index"),
    path("gatos/listar", views.listar_gatos, name="listar_gatos" ),
    path("gatos/salvar", views.salvar_gato, name="cadastrar_gato"),
    path("gatos/salvar/<int:gato_id>/", views.salvar_gato, name="atualizar_gato"),
    path("gatos/excluir/<int:gato_id>/", views.excluir_gato, name="excluir_gato"),
    path("racas/listar", views.listar_racas, name="listar_racas"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_usuario, name="perfil"),
    # path("gatos/<int:gato
]