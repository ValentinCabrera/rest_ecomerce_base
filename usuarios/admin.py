from django.contrib import admin

from .models import Cliente, Domicilio, Localidad, Token

admin.site.register(Cliente)
admin.site.register(Domicilio)
admin.site.register(Localidad)
admin.site.register(Token)
