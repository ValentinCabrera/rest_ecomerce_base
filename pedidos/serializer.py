from rest_framework import serializers
from .models import Pedido, ItemPedido, DetalleItem
from productos.serializer import IngredienteSerializer
from productos.serializer import ProductoSerializer


class DetalleItemSerializer(serializers.ModelSerializer):
    ingrediente = IngredienteSerializer()

    class Meta:
        model = DetalleItem
        fields = '__all__'


class ItemPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    detalles_item = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = '__all__'

    def get_detalles_item(self, obj):
        detalles = obj.get_detalles()
        serializer = DetalleItemSerializer(detalles, many=True)

        return serializer.data

    def get_total(self, obj):
        return obj.get_total()


class PedidoSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    fecha_confirmacion = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = '__all__'
        ordering = ['-id']

    def get_items(self, obj):
        items = obj.get_items()
        serializer = ItemPedidoSerializer(items, many=True)
        return serializer.data

    def get_total(self, obj):
        return obj.get_total()
    
    def get_fecha_confirmacion(self, obj):
        return obj.get_fecha_confirmacion()
