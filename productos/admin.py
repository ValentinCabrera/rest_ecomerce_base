from django.contrib import admin
from .models import Categoria, Producto, DetalleIngrediente, Ingrediente

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(DetalleIngrediente)
admin.site.register(Ingrediente)
