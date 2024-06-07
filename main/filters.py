import django_filters
from main.models import Producto

class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = Producto
        fields = {
            'nombre': ['icontains']
        }