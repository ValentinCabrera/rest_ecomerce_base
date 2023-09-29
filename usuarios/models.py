from django.db import models

from django.contrib.auth.hashers import make_password, check_password
import uuid
from main.models import Estado


class User(models.Model):
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def verify_password(self, password):
        return check_password(password, self.password)

    def full_clean(self, *args, **kwargs):
        try:
            user = User.objects.get(id=self.id)
            if self.password != user.password:
                self.set_password(self.password)

        except:
            self.set_password(self.password)

        super().full_clean(*args, **kwargs)

    def create_token(self):
        token = Token(user=self)
        token.save()

        return token

    def get_token(self):
        tokens = self.token.all()
        return tokens[0] if len(tokens) == 1 else self.create_token()


class Token(models.Model):
    key = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="token")

    def __str__(self):
        return str(self.key)


class Localidad(models.Model):
    localidad = models.CharField(max_length=40)

    def __str__(self):
        return self.localidad


class Departamento(models.Model):
    torre = models.PositiveBigIntegerField()
    codigo = models.CharField(max_length=10)
    piso = models.PositiveSmallIntegerField()


class Domicilio(models.Model):
    localidad = models.ForeignKey(Localidad, on_delete=models.RESTRICT)
    calle = models.CharField(max_length=40)
    numero = models.PositiveSmallIntegerField()
    edificio = models.ForeignKey(
        Departamento, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.calle + ' ' + str(self.numero)


class Cliente(User):
    telefono = models.PositiveBigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40, blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)
    nacimiento = models.DateField(blank=True, null=True)
    domicilio = models.ForeignKey(
        Domicilio, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        nombre_completo = self.nombre
        if self.apellido:
            nombre_completo += ' ' + self.apellido

        return nombre_completo

    def get_pedidos_actuales(self):
        pedidos = self.pedidos.all()
        actuales = list(filter(
            lambda pedido: pedido.get_actual_state().nombre in ["cocinando", "listo"], pedidos))
        
        return actuales[::-1]

    def get_pedidos_historicos(self):
        pedidos = self.pedidos.all()
        historicos = list(filter(
            lambda pedido: pedido.get_actual_state().nombre in ["entregado"], pedidos))

        return historicos[::-1]

    def get_actual_pedido(self):
        pedido = self.pedidos.last()
        estado_pidiendo = Estado.objects.filter(nombre="pidiendo").first()

        if pedido and pedido.get_actual_state() == estado_pidiendo:
            return pedido

        return None


class Cadete(models.Model):
    nombre = models.CharField(max_length=40)
