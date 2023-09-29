from django.contrib import admin

from .models import Pedido, ItemPedido, CambioEstado

admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(CambioEstado)
