from rest_framework import serializers
from shopping_cart.models import DetalleCarritoProducto, CarritoUsuario
from main.models import ImagenProducto


class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ['imagen']
        depth = 1


class DetalleCarritoProductoSerializer(serializers.ModelSerializer):
    imagenproducto = ImagenProductoSerializer(source="producto.imagenproducto_set.first", read_only=True)
    class Meta:
        model = DetalleCarritoProducto
        fields = [
            'id',
            'producto',
            'imagenproducto',
            'talla',
            'cantidad',
            'total'
        ]
        depth = 1


class CarritoUsuarioSerializer(serializers.ModelSerializer):
    detalles = DetalleCarritoProductoSerializer(source="detallecarritoproducto_set", many=True, read_only=True)
    class Meta:
        model = CarritoUsuario
        fields = "__all__"
        depth = 1