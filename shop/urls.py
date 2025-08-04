from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from django.conf import settings

from products.views import *  
from users.views import *  
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductAPIView)
router.register(r'basket', BasketAPIView, basename='basket')
router.register(r'entrance', UserAuthAPIView, basename='entrance')
router.register(r'profile', UserProfileAPIView)    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
# --------------------------------API-------------------------------#
    path('api/', include(router.urls)),
    path('api/shop_auth/', include('rest_framework.urls')),  #подключение авторизации в drf
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),#для входа пользователя по токену адрес будет: auth/token/login/ 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)