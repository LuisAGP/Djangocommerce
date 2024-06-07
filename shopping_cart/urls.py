from django.urls import path
from .views import *

urlpatterns = [
    path('agregar_producto/', AgregarProducto.as_view(), name="agregar_producto"),
    path('carrito/', CarritoView.as_view(), name="carrito"),
]