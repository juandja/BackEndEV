from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContabilidadView
from .views import ProductoViewSet, MovimientoInventarioViewSet, TransaccionViewSet
from django.urls import path
from . import views  # Asegúrate de que esta línea está presente
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductoImagenUploadView


router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoInventarioViewSet)
router.register(r'transacciones', TransaccionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("contabilidad/", ContabilidadView.as_view(), name="contabilidad"),
    path('productos-publicos/', views.productos_publicos, name='productos-publicos'),
    path('api/productos/<int:pk>/imagen/', ProductoImagenUploadView.as_view(), name='producto-imagen-upload'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)