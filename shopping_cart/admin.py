from django.contrib import admin
from .models import *

class CarritoUsuarioAdmin(admin.ModelAdmin):
    pass

class DetalleCarritoProductoAdmin(admin.ModelAdmin):
    pass

admin.site.register(CarritoUsuario, CarritoUsuarioAdmin)
admin.site.register(DetalleCarritoProducto, DetalleCarritoProductoAdmin)