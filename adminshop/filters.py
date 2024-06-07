import django_filters
from django.db.models import Q
from main.models import Producto

class ProductoFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(method='product_filter', label="search")

    class Meta:
        model = Producto
        fields = ['q']

    def product_filter(self, queryset, name, value):
        return queryset.filter(
            Q(nombre__icontains=value) |
            Q(codigo__icontains=value) | 
            Q(genero__icontains=value)
        )