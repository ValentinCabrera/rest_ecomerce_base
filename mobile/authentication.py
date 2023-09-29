from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from usuarios.models import Token


class UserAutenticacion(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token is not None and token.startswith('Token '):
            key = token[6:]

        else:
            raise AuthenticationFailed(
                'No se proporcionó un token de autenticación.')

        try:
            token = Token.objects.get(key=key)

        except:
            raise AuthenticationFailed('Token de autenticación no válido.')

        return (token.user, None)
