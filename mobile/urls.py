from django.urls import path
from mobile.views.login import *
from mobile.views.pedido import *

app_name = 'mobile'

urlpatterns = [
    path('login/login/', Login.as_view()),
    path('login/verify/', VerifyToken.as_view()),
    path('pedido/get/', GetPedido.as_view()),
    path('pedido/get/all/', GetAllPedidos.as_view()),
    path('pedido/item/add/', AddItem.as_view()),
    path('pedido/item/remove/', RemoveItem.as_view()),
    path('pedido/item/delete/', DeleteItem.as_view()),
    path('pedido/confirmar/', ConfirmarPedido.as_view()),
    path('pedido/repetir/', RepetirPedido.as_view()),
]
