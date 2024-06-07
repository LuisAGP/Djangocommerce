from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from shopping_cart.models import CarritoUsuario, DetalleCarritoProducto
from .serializers import CarritoUsuarioSerializer, DetalleCarritoProductoSerializer

class DetallesCarritoView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DetalleCarritoProductoSerializer
    queryset = DetalleCarritoProducto.objects.all()
    
    def put(self, request, id):
        detalle = DetalleCarritoProducto.objects.get(id=id)
        serializer = DetalleCarritoProductoSerializer(detalle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarritoView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CarritoUsuarioSerializer

    def get_queryset(self):
        carrito = CarritoUsuario.objects.prefetch_related('detallecarritoproducto_set').filter(user=self.request.user)
        return carrito
    