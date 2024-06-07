from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from main.models import Producto, Categoria, TallaProducto
from django.contrib import messages
from .filters import ProductoFilter
import json


def home_view(request):
    try:
        productos = Producto.objects.all()
        productos_filter = ProductoFilter(request.GET, queryset=productos)
        paginator = Paginator(productos_filter.qs, 20)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'productos': page_obj,
            'productos_filter': productos_filter,
            'categorias': Categoria.objects.all()
        }

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")

    return render(request, 'views/home.html', context)


def detalle_producto_view(request,id):
    try:
        producto = Producto.objects.get(id=id)

        context = {
            'producto': producto
        }

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")

    return render(request, 'views/detalle_producto.html', context)


def get_stock(request):
    if request.method == "POST" and 'id_talla' in request.POST:
        talla = TallaProducto.objects.get(id=request.POST['id_talla'])

        response = { "stock": talla.stock, "code": 200 }
    else:
        response = { "message": "Algo salió mal", "code": 500 }


    return HttpResponse(json.dumps(response, indent=4, sort_keys=True, default=str), content_type="application/json")
