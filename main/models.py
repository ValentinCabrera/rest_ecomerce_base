from django.db import models


class Estado(models.Model):
    """
    Pedido = [pidiendo, cocinando, listo, entregado, cancelado]

    """
    nombre = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.nombre
