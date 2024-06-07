from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_panel_view, name='admin_panel'),
    path('nuevo_producto/', nuevo_producto_view, name='nuevo_producto'),
    path('todos_productos/', consulta_productos_view, name="todos_productos"),
    path('eliminar_producto/', eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<str:id>', editar_producto_view, name="editar_producto"),
    path('guardar_categoria/', guardar_categoria_view, name='guardar_categoria'),
    path('eliminar_categoria/', eliminar_categoria, name='eliminar_categoria'),
    path('eliminar_imagen_producto/', eliminar_imagen_producto, name='eliminar_imagen_producto')
]