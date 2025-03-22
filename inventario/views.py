from django.shortcuts import render
from rest_framework.views import APIView
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
                producto.stock -= transaccion.cantidad  # Se vendió un producto, baja el stock
            elif transaccion.tipo == "gasto":
                producto.stock += transaccion.cantidad  # Se compró más stock, aumenta

            producto.save()
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
        total_ingresos = Transaccion.objects.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
        total_gastos = Transaccion.objects.filter(tipo='gasto').aggregate(total=Sum('monto'))['total'] or 0
        ganancia_neta = total_ingresos - total_gastos

        resumen_financiero = {
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "ganancia_neta": ganancia_neta
        }

        transacciones = Transaccion.objects.all().order_by('-fecha')
        paginator = TransaccionPagination()
        paginated_transacciones = paginator.paginate_queryset(transacciones, request)
        transacciones_serializadas = TransaccionSerializer(paginated_transacciones, many=True)

        return paginator.get_paginated_response({
            "message": "Acceso permitido",
            "resumen_financiero": resumen_financiero,
            "transacciones": transacciones_serializadas.data
        })

# Create your views here.


