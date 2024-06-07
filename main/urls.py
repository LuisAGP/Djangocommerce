from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('detalle_producto/<str:id>', detalle_producto_view, name="detalle_producto"),
    path('get_stock', get_stock, name="get_stock"),
]