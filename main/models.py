from django.db import models
import uuid
from .const import GENERO, TALLAS


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    identificador = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('nombre',)
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
    
    def __str__(self):
        return self.nombre
    


class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    categoria = models.ForeignKey(Categoria, related_name='productos',on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, db_index=True)
    codigo = models.CharField(max_length=255, db_index=True)
    genero = models.CharField(max_length=50,choices=GENERO)
    descripcion = models.TextField(blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nombre',)
        index_together = (('id', 'codigo'),)

    def __str__(self):
        return self.nombre
    
    def imagen_portada(self):
        portada = ImagenProducto.objects.filter(producto=self).first()
        return portada
    


def upload_location(instance, filename):
    return f'products/{instance.producto.id}/{filename}'


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=upload_location)
    


class TallaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.DecimalField(max_digits=5, decimal_places=1, choices=TALLAS)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.talla}"

