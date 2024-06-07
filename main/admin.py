from django.contrib import admin
from .models import *

class CategoriaAdmin(admin.ModelAdmin):
    pass

class ProductoAdmin(admin.ModelAdmin):
    pass

class ImagenProductoAdmin(admin.ModelAdmin):
    pass

class TallaProductoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ImagenProducto, ImagenProductoAdmin)
admin.site.register(TallaProducto, TallaProductoAdmin)
