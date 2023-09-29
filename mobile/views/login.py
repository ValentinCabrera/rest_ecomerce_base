from rest_framework.views import APIView
from usuarios.models import Cliente
from usuarios.serializer import TokenSerializer, ClienteSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from mobile.authentication import UserAutenticacion
from mobile.permissions import UserPermisions


class Login(APIView):
    def post(self, request):
        try:
            telefono = int(request.data.get("user"))
            password = request.data.get("password")

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cliente = get_object_or_404(Cliente, telefono=telefono)

        if cliente.verify_password(password):
            token = cliente.get_token()
            serializer = TokenSerializer(token)

            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class VerifyToken(APIView):
    authentication_classes = [UserAutenticacion]
    permission_classes = [UserPermisions]

    def get(self, request):
        cliente = request.user.cliente
        serializer = ClienteSerializer(cliente)

        return Response(serializer.data)
