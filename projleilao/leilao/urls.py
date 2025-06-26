from django.urls import path
import leilao.views as views
app_name = "leilao"
urlpatterns = [
    path("", views.index, name="index"),
    path("leiloes/<int:leilao_id>/itens", views.listar_itensLeilao, name="listar_itens"),
    #path("gatos/listar", views.listar_gatos, name="listar_gatos" ),
]