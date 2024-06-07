from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .filters import ProductoFilter
from main.models import Categoria, Producto, ImagenProducto, TallaProducto
from main.const import GENERO, TALLAS
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json


# Vista principal del panel de administración
@login_required
def admin_panel_view(request):
    if not request.user.is_superuser:
        return redirect('home')

    return render(request, 'views/admin_panel.html', {})


# Vista para guardar un nuevo producto
@login_required
def nuevo_producto_view(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    try:

        #INIT##################### CONSULTA DE INFORMACIÓN NECESARIA ##########################

        context = {
            'categorias': Categoria.objects.all(),
            'generos': GENERO,
            'tallas': TALLAS
        }

        #END###################### CONSULTA DE INFORMACIÓN NECESARIA ##########################


        if request.method == "POST":

            #INIT##################### CREACIÓN DE INSTANCIA PRODUCTO ##########################

            producto = Producto()
            categoria = Categoria.objects.get(identificador=request.POST['categoria'])

            producto.categoria = categoria
            producto.nombre = request.POST['nombre']
            producto.codigo = request.POST['codigo']
            producto.descripcion = request.POST['descripcion']
            producto.genero = request.POST['genero']
            producto.precio_venta = request.POST['precio_venta']
            producto.precio_compra = request.POST['precio_compra']
            producto.stock = request.POST['stock']

            producto.save()

            #END###################### CREACIÓN DE INSTANCIA PRODUCTO ##########################



            #INIT################# CREACIÓN DE INSTANCIA IMAGEN PRODUCTO #######################

            for i in request.FILES.getlist('imagen'):
                imagen = ImagenProducto()
                imagen.imagen = i
                imagen.producto = producto
                imagen.save()

            #END################## CREACIÓN DE INSTANCIA IMAGEN PRODUCTO #######################



            #INIT################## CREACIÓN DE INSTANCIA TALLA PRODUCTO #######################
            
            tallas = request.POST.getlist('tallas[]')
            stock_tallas = request.POST.getlist('stock_talla[]')

            for i in range(len(tallas)):
                talla = TallaProducto()
                talla.producto = producto
                talla.talla = tallas[i]
                talla.stock = stock_tallas[i]
                talla.save()

            #END################### CREACIÓN DE INSTANCIA TALLA PRODUCTO #######################


            messages.success(request, f"Producto guardado con exito!")
            response = { "message": "Producto guardado correctamente!", "code": 200 }

            return HttpResponse(json.dumps(response, indent=4, sort_keys=True, default=str), content_type="application/json")
    except Exception as e:
        response = { "message": f"Algo salio mal! {e}", "code": 500 }
        return HttpResponse(json.dumps(response, indent=4, sort_keys=True, default=str), content_type="application/json")

    return render(request, 'views/nuevo_producto.html', context)


@login_required
def consulta_productos_view(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    productos = Producto.objects.all()
    productos_filter = ProductoFilter(request.GET, queryset=productos)
    paginator = Paginator(productos_filter.qs, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'productos': page_obj,
        'productos_filter': productos_filter
    }

    return render(request, 'views/todos_productos.html', context)


@login_required
def eliminar_producto(request):
    try:
        if not request.user.is_superuser:
            raise "Debes ser administrador para realizar esta acción"
        if request.method != "POST":
            raise "Error al procesar la solicitud"
        id = request.POST['id_producto']
        producto = Producto.objects.get(id=id)
        producto.delete()

        context = {
            'productos': Producto.objects.all()
        }

        messages.success(request, f"Producto eliminado correctamente!")

        return redirect('todos_productos')

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")
    
    return render(request, 'views/todos_productos.html', context)


@login_required
def editar_producto_view(request, id):
    if not request.user.is_superuser:
        return redirect('home')

    try:
        if request.method == "POST":
            producto = Producto.objects.get(id=id)
            categoria = Categoria.objects.get(identificador=request.POST['categoria'])

            producto.categoria = categoria
            producto.nombre = request.POST['nombre']
            producto.codigo = request.POST['codigo']
            producto.descripcion = request.POST['descripcion']
            producto.genero = request.POST['genero']
            producto.precio_venta = request.POST['precio_venta']
            producto.precio_compra = request.POST['precio_compra']
            producto.stock = request.POST['stock']

            producto.save()

            for i in request.FILES.getlist('imagen'):
                imagen = ImagenProducto()
                imagen.imagen = i
                imagen.producto = producto
                imagen.save()

            tallas = request.POST.getlist('tallas[]')
            stock_tallas = request.POST.getlist('stock_talla[]')

            for i in range(len(tallas)):
                talla = TallaProducto.objects.get(id=tallas[i])
                talla.producto = producto
                talla.stock = stock_tallas[i]
                talla.save()

            messages.success(request, f"Producto guardado con exito!")

            response = { "message": "Producto guardado correctamente!", "code": 200 }

            return HttpResponse(json.dumps(response, indent=4, sort_keys=True, default=str), content_type="application/json")
    except Exception as e:
        response = { "message": f"Algo salio mal! {e}", "code": 500 }
        return HttpResponse(json.dumps(response, indent=4, sort_keys=True, default=str), content_type="application/json")

    producto = Producto.objects.get(id=id)

    context = {
        'producto': producto,
        'categorias': Categoria.objects.all(),
        'generos': GENERO,
        'tallas': TallaProducto.objects.filter(producto=producto)
    }

    return render(request, 'views/editar_producto.html', context)



@login_required
def guardar_categoria_view(request):
    if not request.user.is_superuser:
        return redirect('home')

    try:
        if request.method == "POST" and request.POST['nombre'] != "":

            identificador = str(request.POST['nombre']).strip().lower()
            identificador.replace('á', 'a')
            identificador.replace('é', 'e')
            identificador.replace('í', 'i')
            identificador.replace('ó', 'o')
            identificador.replace('ú', 'u')

            categoria = Categoria()
            categoria.nombre = request.POST['nombre']
            categoria.identificador = identificador
            categoria.save()

            messages.success(request, f"Se agregó una nueva categoria!")

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")

    context = {
        'categorias': Categoria.objects.all()
    }

    return render(request, 'views/guardar_categoria.html', context)


@login_required
def eliminar_categoria(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    try:
        categoria = Categoria.objects.get(id=request.POST['id_categoria'])
        categoria.delete()

        messages.success(request, f"Se eliminó la categoria correctamente!")
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")

    return redirect('guardar_categoria')



@login_required
def eliminar_imagen_producto(request):
    response = {}

    try:
        if not request.user.is_superuser:
            raise "Debes ser administrador para realizar esta acción"
        
        if request.method == 'POST':
            id_imagen = request.POST['id_imagen']
            imagen = ImagenProducto.objects.get(id=id_imagen)
            imagen.imagen.delete(save=True)
            imagen.delete()

            response = { "message": "Imagen eliminada", "id_imagen": id_imagen, "code": 200 }
            
    except Exception as e:
        response = { "message": str(e), "code": 500 }

    return HttpResponse(json.dumps(response, indent=4, sort_keys=True, default=str), content_type="application/json")