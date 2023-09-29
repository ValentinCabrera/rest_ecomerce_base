from rest_framework.views import APIView
from mobile.permissions import UserPermisions
from mobile.authentication import UserAutenticacion
from rest_framework.response import Response
from pedidos.serializer import PedidoSerializer
from pedidos.models import Pedido
from django.shortcuts import get_object_or_404
from productos.models import Producto


def get_actual_pedido(cliente):
    pedido = cliente.get_actual_pedido()

    if not pedido:
        pedido = Pedido(cliente=cliente)
        pedido.save()

    return pedido


class GetAllPedidos(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def get(self, request):
        cliente = request.user.cliente
        actuales = cliente.get_pedidos_actuales()
        historicos = cliente.get_pedidos_historicos()

        actuales_serializer = PedidoSerializer(actuales, many=True)
        historicos_serializer = PedidoSerializer(historicos, many=True)

        return Response({"actuales": actuales_serializer.data, "historicos": historicos_serializer.data})


class GetPedido(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def get(self, request):
        cliente = request.user.cliente
        pedido = get_actual_pedido(cliente)

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)


class AddItem(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def post(self, request):
        cliente = request.user.cliente
        pedido = get_actual_pedido(cliente)

        producto = get_object_or_404(
            Producto, id=int(request.data.get("producto")))

        cantidad = int(request.data.get("cantidad"))

        pedido.add_item(producto, cantidad)
        serializer = PedidoSerializer(pedido)

        return Response(serializer.data)


class RemoveItem(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def post(self, request):
        cliente = request.user.cliente
        pedido = get_actual_pedido(cliente)

        producto = get_object_or_404(
            Producto, id=int(request.data.get("producto")))
        cantidad = int(request.data.get("cantidad"))

        pedido.remove_item(producto, cantidad)
        serializer = PedidoSerializer(pedido)

        return Response(serializer.data)


class DeleteItem(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def post(self, request):
        cliente = request.user.cliente
        pedido = get_actual_pedido(cliente)

        producto = get_object_or_404(
            Producto, id=int(request.data.get("producto")))

        pedido.delete_item(producto)
        serializer = PedidoSerializer(pedido)

        return Response(serializer.data)


class ConfirmarPedido(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def get(self, request):
        cliente = request.user.cliente
        pedido = get_actual_pedido(cliente)

        pedido.confirmar_pedido()

        return Response({})

class RepetirPedido(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def post(self, request):
        cliente = request.user.cliente
        old_pedido = get_object_or_404(
            Pedido, id=int(request.data.get("pedido")))
        
        pedido = Pedido(cliente=cliente)
        pedido.save()
        pedido.copy(old_pedido)

        actuales = cliente.get_pedidos_actuales()
        historicos = cliente.get_pedidos_historicos()

        actuales_serializer = PedidoSerializer(actuales, many=True)
        historicos_serializer = PedidoSerializer(historicos, many=True)

        return Response({"actuales": actuales_serializer.data, "historicos": historicos_serializer.data})

        