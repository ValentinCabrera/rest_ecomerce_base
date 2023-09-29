from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    imagen = models.ImageField(
        upload_to="productos/static/categorias", blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def get_productos(self):
        return self.productos.all()
    

class Producto(models.Model):
    nombre = models.CharField(max_length=40)
    imagen = models.ImageField(upload_to="productos/static/productos")
    descripcion = models.TextField(blank=True, null=True)
    stock = models.PositiveSmallIntegerField()
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.RESTRICT, related_name="productos")
    precio = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nombre

    def get_ingredientes(self):
        return map(lambda detalle: detalle.ingrediente, self.detalles.all())
    
    def get_precio(self):
        actual = self.precios.last()
        return actual.precio if actual else 0

class HistorialPrecios(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT, related_name='precios')
    precio = models.PositiveSmallIntegerField()

"""class VarianteProducto(models.Model):
    nombre = models.CharField(max_length=40)"""

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=40)
    precio = models.PositiveSmallIntegerField()
    activo = models.BooleanField()


class DetalleIngrediente(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.RESTRICT, related_name="detalles")
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.RESTRICT)