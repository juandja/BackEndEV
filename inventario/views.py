from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Producto, MovimientoInventario, Transaccion
from .serializers import ProductoSerializer, MovimientoInventarioSerializer, TransaccionSerializer
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ProductoImagen



@api_view(['GET'])
@permission_classes([]) # Esto permite acceso sin autenticación
def productos_publicos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def es_admin(user):
    return user.is_superuser

def home(request):
    return HttpResponse("Bienvenido a la API de Inventario y Finanzas")

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    # Agregar filtros y búsquedas
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fecha_creacion', 'precio']  # Filtrar por estos campos
    search_fields = ['nombre', 'descripcion']  # Buscar en estos campos
    ordering_fields = ['precio', 'stock']  # Ordenar por estos campos

class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        transaccion = serializer.save()
        print(f"Transacción creada: {transaccion.descripcion}, Tipo: {transaccion.tipo}, Cantidad: {transaccion.cantidad}")

        if hasattr(transaccion, 'producto') and hasattr(transaccion, 'cantidad'):
            producto = transaccion.producto
            print(f"Producto antes de actualizar stock: {producto.nombre}, Stock: {producto.stock}")

            if transaccion.tipo == "ingreso":
                if producto.stock < transaccion.cantidad:
                 raise ValidationError({"error": f"Stock insuficiente para vender {transaccion.cantidad} {producto.nombre}. Stock actual: {producto.stock}"})
                
                producto.stock -= transaccion.cantidad  # Se vendió stock
                transaccion.descripcion = f"Venta de {transaccion.cantidad} {producto.nombre}"
                
            elif transaccion.tipo == "gasto":
                producto.stock += transaccion.cantidad  # Se compró más stock, aumenta
                transaccion.descripcion = f"Compra de {transaccion.cantidad} {producto.nombre}"
                

            producto.save()
            transaccion.save()
            print(f"Producto después de actualizar stock: {producto.nombre}, Stock: {producto.stock}")


def es_admin(user):
    return user.is_superuser

@user_passes_test(es_admin)
def contabilidad_view(request):
    ingresos = Transaccion.objects.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    gastos = Transaccion.objects.filter(tipo='gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    ganancia = ingresos - gastos
    
    contexto = {
        'ingresos': ingresos,
        'gastos': gastos,
        'ganancia': ganancia,
    }
    return render(request, 'contabilidad/resumen.html', contexto)            

class TransaccionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContabilidadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Calcular ingresos (ventas de productos)
        ingresos = Transaccion.objects.filter(tipo='ingreso').values('producto__nombre').annotate(total=Sum('monto'))
        total_ingresos = sum(item['total'] for item in ingresos if item['total'] is not None)
        
        # Calcular gastos (compras de inventario o inversiones)
        gastos = Transaccion.objects.filter(tipo='gasto').values('producto__nombre').annotate(total=Sum('monto'))
        total_gastos = sum(item['total'] for item in gastos if item['total'] is not None)
        
        # Calcular ganancia neta
        ganancia_neta = total_ingresos - total_gastos
        
        resumen_financiero = {
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "ganancia_neta": ganancia_neta,
            "detalle_ingresos": list(ingresos),
            "detalle_gastos": list(gastos)
        }

        return Response(resumen_financiero)
    
class ProductoImagenUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, pk, format=None):
        try:
            producto = Producto.objects.get(pk=pk)  # Verificar que el producto existe
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if 'imagen' not in request.data:
            return Response({"error": "No se ha enviado ninguna imagen"}, status=status.HTTP_400_BAD_REQUEST)

        producto_imagen = ProductoImagen(producto=producto, imagen=request.data['imagen'])
        producto_imagen.save()
        
        # Actualizar el campo imagen del producto con la última imagen subida
        producto.imagen = producto_imagen.imagen
        producto.save()
        
        # Devolver la URL de la imagen en la respuesta
        imagen_url = request.build_absolute_uri(producto_imagen.imagen.url)
        
        return Response({
            "message": "Imagen subida exitosamente",
            "imagen_url": imagen_url
        }, status=status.HTTP_201_CREATED)


# Create your views here.

