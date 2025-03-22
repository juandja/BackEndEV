from django.db import models

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # Stock del producto
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

# Modelo de Movimiento de Inventario
class MovimientoInventario(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

# Modelo de Transacción Financiera
class Transaccion(models.Model):
    TIPO_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    )
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con Producto
    cantidad = models.PositiveIntegerField()  # Cantidad de productos en la transacción
    
##def save(self, *args, **kwargs):
  ##      """Actualizar stock automáticamente cuando se guarda la transacción"""
    ##    if self.pk is None:  # Solo afecta nuevas transacciones
      ##      if self.tipo == 'ingreso':
        ##        self.producto.stock -= self.cantidad  # Venta reduce stock
          ##  elif self.tipo == 'gasto':
            ##    self.producto.stock += self.cantidad  # Compra aumenta stock
           ## self.producto.save()
        ##super().save(*args, **kwargs)

def __str__(self):
        return f"{self.tipo}: {self.descripcion} - ${self.monto}"