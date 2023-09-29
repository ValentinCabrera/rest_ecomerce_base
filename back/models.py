from django.db import models


class Estado(models.Model):
    """
    Pedido = [pidiendo, cocinando, enviando]

    """
    nombre = models.CharField(max_length=40, unique=True)

    def are_you(self, name):
        return self.nombre == name

    def __str__(self):
        return self.nombre
