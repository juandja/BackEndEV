from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContabilidadView
from .views import ProductoViewSet, MovimientoInventarioViewSet, TransaccionViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoInventarioViewSet)
router.register(r'transacciones', TransaccionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', include(router.urls)),
    path("contabilidad/", ContabilidadView.as_view(), name="contabilidad"),
]