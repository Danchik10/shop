from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

from products.views import *    
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
# --------------------------------API-------------------------------#
    path('api/', include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)