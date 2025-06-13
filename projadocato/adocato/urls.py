from django.urls import path
import adocato.views as views
app_name = "adocato"
urlpatterns = [
    path("", views.index, name="index"),
    path("gatos/listar", views.listar_gatos, name="listar_gatos" ),
]