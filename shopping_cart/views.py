from django.shortcuts import render
from django.views import View
from .models import *
from djcommerce.utils import json_response, get_error_info
from django.db.models import Sum

class AgregarProducto(View):
    def recalcular_carrito(self, carrito):
        detalles = DetalleCarritoProducto.objects.filter(carrito=carrito)

        cantidad_total = 0
        importe_total = 0

        for i in detalles:
            cantidad_total += i.cantidad
            importe_total += i.total

        carrito.cantidad_productos =  cantidad_total
        carrito.importe_total = importe_total
        carrito.save()

    def post(self, request):
        if not request.user.is_authenticated:
            response = {'message': "Debe iniciar sesión", 'code': 500}
            return json_response(response)
        
        producto = Producto.objects.get(id=request.POST['id_producto'])
        talla = TallaProducto.objects.get(id=request.POST['id_talla'])
        cantidad = int(request.POST['cantidad'])

        try:
            carrito, created = CarritoUsuario.objects.get_or_create(user=request.user)
            if not created:
                detalles, created = DetalleCarritoProducto.objects.get_or_create(carrito=carrito, producto=producto, talla=talla)
                
                if not created:
                    detalles.cantidad += cantidad
                    detalles.total += cantidad*producto.precio_venta
                else:
                    detalles.cantidad = cantidad
                    detalles.total = cantidad*producto.precio_venta

                detalles.save()
            else:
                detalles = DetalleCarritoProducto()
                detalles.carrito = carrito
                detalles.talla = talla
                detalles.cantidad = cantidad
                detalles.total = cantidad*producto.precio_venta
                detalles.save()
            
            carrito.save()
            self.recalcular_carrito(carrito)

            response = {'message': "Se agregó el producto al carrito!", 'code': 200}

        except Exception as e:
            tipo,nombre,linea = get_error_info(e)
            print(tipo,nombre,linea)
            response = {'message': "Ocurrió un error inesperado", 'err': e, 'l': linea, 'code': 500}

        return json_response(response)
            

class CarritoView(View):
    def get(self, request):
        if not request.user.carritousuario_set.first():
            return render(request, 'views/carrito.html', {'carrito': False})

        carrito = request.user.carritousuario_set.first()
        detalles = carrito.detallecarritoproducto_set.all()
        subtotal = detalles.aggregate(subtotal=Sum('cantidad')*Sum('producto__precio_venta'))['subtotal']
        
        context = {
            'carrito': carrito,
            'detalles': detalles,
            'subtotal': subtotal,
            'total': subtotal+carrito.precio_envio
        }

        return render(request, 'views/carrito.html', context)
    

    def put(self, request, id):
        print(request, id)

        return json_response({"message": "process"})
