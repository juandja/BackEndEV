from rest_framework import serializers
from .models import Producto, MovimientoInventario, Transaccion

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'

        def validate_producto(self, value):
            print(f"Producto recibido en el serializador: {value}")
            return value