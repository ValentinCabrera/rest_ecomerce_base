from django.db import models
from usuarios.models import Cliente, Cadete
from productos.models import Producto, Ingrediente
from main.models import Estado


class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.RESTRICT, blank=True, null=True, related_name="pedidos")
    cadete = models.ForeignKey(
        Cadete, on_delete=models.RESTRICT, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Pedido, self).save(*args, **kwargs)

        pidiendo = Estado.objects.get(nombre="pidiendo")
        c = CambioEstado(pedido=self, estado=pidiendo)
        c.save()

    def __str__(self):
        return str(self.id)
    
    def copy(self, old):
        items = old.get_items()

        for i in items:
            item = ItemPedido(pedido=self, producto=i.producto, cantidad=i.cantidad)
            item.save()
        
        self.confirmar_pedido()

    def get_items(self):
        return self.items.all()

    def get_total(self):
        items = self.get_items()

        total = 0

        for item in items:
            total += item.get_precio() * item.cantidad

        return total

    def get_actual_state(self):
        return self.cambios_estado.last().estado

    def add_item(self, producto, cantidad=1):
        existe_item = self.items.filter(producto=producto).first()

        if existe_item:
            existe_item.cantidad += cantidad
            existe_item.save()

        else:
            i = ItemPedido(pedido=self, producto=producto, cantidad=cantidad)
            i.save()

    def remove_item(self, producto, cantidad=1):
        item = self.items.filter(producto=producto).first()

        if item.cantidad - cantidad > 0:
            item.cantidad -= cantidad
            item.save()

        else:
            item.delete()

    def delete_item(self, producto):
        item = self.items.filter(producto=producto).first()
        item.delete()

    def confirmar_pedido(self):
        estado_cocinando = Estado.objects.get(nombre="cocinando")
        CambioEstado(pedido=self, estado=estado_cocinando).save()

    def get_fecha_confirmacion(self):
        cambios = list(filter(lambda cambio: cambio.estado.nombre == "cocinando", self.cambios_estado.all()))
        
        if len(cambios) > 0:
            fecha_hora = cambios[0].fecha_hora
            fecha_formateada = {}

            for i in [["mes",'%d'], ["dia",'%b'], ["hora",'%H'], ["minuto",'%M']]:
                fecha_formateada[i[0]] = fecha_hora.strftime(i[1])

            return fecha_formateada

        return None

class CambioEstado(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="cambios_estado")
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_hora = models.DateTimeField(auto_now=True)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.PositiveSmallIntegerField()

    def get_total(self):
        return self.producto.precio * self.cantidad

    def get_item(self):
        return {"producto": self.producto, "cantidad": self.cantidad}

    def get_precio(self):
        detalles = map(lambda detalle: detalle.ingrediente.precio *
                       (detalle.cantidad - 1), self.detalles.all())

        sub_total = self.producto.precio + sum(detalles)
        return sub_total

    def get_detalles(self):
        detalles = self.detalles.all()
        return detalles


class DetalleItem(models.Model):
    item_pedido = models.ForeignKey(
        ItemPedido, on_delete=models.CASCADE, related_name="detalles")
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.RESTRICT)
    cantidad = models.PositiveSmallIntegerField()
