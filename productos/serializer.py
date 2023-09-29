from rest_framework import serializers
from .models import Categoria, Producto, Ingrediente, Catalogo, CategoriaCatalogo, ItemCatalogo


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = '__all__'

    def get_productos(self, obj):
        productos = obj.get_productos()
        serializer = ProductoSerializer(productos, many=True)
        return serializer.data


class ProductoSerializer(serializers.ModelSerializer):
    ingredientes = serializers.SerializerMethodField()
    precio = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'

    def get_ingredientes(self, obj):
        ingredientes = obj.get_ingredientes()
        serializer = IngredienteSerializer(ingredientes, many=True)

        return serializer.data
    
    def get_precio(self, obj):
        return obj.get_precio()