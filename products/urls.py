from django.urls import path

from products.views import products, basket_add, basket_remove
from products.views import ProductAPIView

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>', products, name='category'),
    path('page/<int:page_number>', products, name='paginator'),
    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>', basket_remove, name='basket_remove'),
# --------------------------------API-------------------------------#
    # path('productlist/', ProductAPIView.as_view({'get' : 'list'})),
    # path('productlist/<int:pk>/', ProductAPIView.as_view({'put' : 'update'})),
]