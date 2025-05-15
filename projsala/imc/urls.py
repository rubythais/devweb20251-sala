from django.urls import path
from . import views
app_name = 'imc'
urlpatterns=[
    path('',views.index,name='index'),
    path("processar/", views.calcular_imc_view, name = "calcular_imc"),
]