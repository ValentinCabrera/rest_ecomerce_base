from django.urls import path
from .views import *

app_name = 'productos'

urlpatterns = [
    path('categorias/', GetCategorias.as_view()),
]
