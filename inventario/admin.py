from django.contrib import admin
from .models import Producto, MovimientoInventario, Transaccion

admin.site.register(Producto)
admin.site.register(MovimientoInventario)
admin.site.register(Transaccion)