from django.urls import path, include
from .views import CarritoView, DetallesCarritoView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'carrito', CarritoView, 'carrito')
router.register(r'detallecarrito', DetallesCarritoView, 'detallecarrito')

urlpatterns = [
    path('v1/', include(router.urls))
]