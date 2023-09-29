from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Cliente
from .serializer import TokenSerializer


class Login(APIView):
    def post(self, request):
        cliente = get_object_or_404(Cliente, nombre=request.data.get("user"))
        password = request.data.get("password")

        if cliente.verify_password(password):
            token = cliente.get_token()
            serializer = TokenSerializer(token)

            return Response({"token": serializer.data})

        else:
            return Response({"detail": "Not found."})
