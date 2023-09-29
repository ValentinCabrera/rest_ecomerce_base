from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Categoria, Producto, Catalogo
from .serializer import CategoriaSerializer, ProductoSerializer, CatalogoSerializer

class GetCategorias(APIView):
    """
    Listar categorias
    """

    def get(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data)