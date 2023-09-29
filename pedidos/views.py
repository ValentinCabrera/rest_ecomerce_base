from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Pedido, ItemPedido, DetalleItem
from .serializer import PedidoSerializer
from productos.models import Producto, Ingrediente


class CrearPedido(APIView):
    """
    Crear un nuevo pedido

    return: pedido
    """

    def get(self, request):
        pedido = Pedido()
        pedido.save()

        serializer = PedidoSerializer(pedido)

        return Response(serializer.data)


class ConfirmarPedido(APIView):
    """
    Confirmar un pedido

    args: pedido
    returns: pedido
    """

    def post(self, request):
        pedido = get_object_or_404(Pedido, pk=int(request.data.get("pedido")))
        pedido.pasar_cocina()

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)


class ModificarCantidad(APIView):
    def post(self, request):
        cantidad = int(request.data.get("cantidad"))
        item = get_object_or_404(ItemPedido, pk=int(request.data.get("item")))
        item.cantidad += cantidad
        item.save()

        if cantidad == 0 or item.cantidad == 0:
            item.delete()

            # borrar items primero

        pedido = item.pedido
        serializer = PedidoSerializer(pedido)

        return Response(serializer.data)


class AgregarProducto(APIView):
    """
    Agregar un producto al pedido

    args: pedido, producto, cantidad
    return: pedido
    """

    def post(self, request):
        pedido = get_object_or_404(Pedido, pk=int(request.data.get("pedido")))
        producto = get_object_or_404(
            Producto, pk=int(request.data.get("producto")))
        cantidad = int(request.data.get("cantidad"))
        raw_ingredientes = request.data.get("ingredientes")

        def existe():
            items = ItemPedido.objects.filter(
                pedido=pedido, producto=producto)

            if items.count() == 0:
                return False

            def verificar_item(item):
                detalles = []

                for i in raw_ingredientes:
                    ingrediente = get_object_or_404(
                        Ingrediente, pk=int(i["ingrediente"]["id"]))

                    try:
                        detalle = DetalleItem.objects.get(
                            item_pedido=item, ingrediente=ingrediente, cantidad=int(i["cantidad"]))
                        detalles.append(detalle)

                    except:
                        pass

                if len(raw_ingredientes) == len(item.get_detalles()):
                    for i in item.get_detalles():
                        if i not in detalles:
                            return False

                else:
                    return False

                return True

            for item in items:
                if verificar_item(item):
                    return item

            return False

        if existe():
            item = existe()
            item.cantidad += 1
            item.save()

        else:
            item = ItemPedido(
                pedido=pedido, producto=producto, cantidad=cantidad)
            item.save()

        for i in raw_ingredientes:
            ingrediente = get_object_or_404(
                Ingrediente, pk=int(i["ingrediente"]["id"]))

            detalle = DetalleItem(
                item_pedido=item, ingrediente=ingrediente, cantidad=int(i["cantidad"]))
            detalle.save()

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)
