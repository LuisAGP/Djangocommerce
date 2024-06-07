from django.db import models
from main.models import Producto, TallaProducto
from users.models import User
import uuid

class CarritoUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad_productos = models.IntegerField(default=0)
    importe_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    precio_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.user.email}"

class DetalleCarritoProducto(models.Model):
    carrito = models.ForeignKey(CarritoUsuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="productos_carrito")
    talla = models.ForeignKey(TallaProducto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Detalle {self.carrito.user} - {self.producto}:{self.talla}"