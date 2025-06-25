from django.urls import path
import leilao.views as views
app_name = "leilao"
urlpatterns = [
    path("", views.index, name="index"),
    #path("gatos/listar", views.listar_gatos, name="listar_gatos" ),
]