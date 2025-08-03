from rest_framework import serializers
from .models import Product, ProductsCategory
   

class ProductSerializer(serializers.ModelSerializer):    #класс засчёт которого происходит весь функционал(преобразование в json, создание, изменение записей в бд)
    #благодаря нему не нужно прописывать отдельно атрибуты из models.py
    class Meta:
        model = Product
        fields = '__all__'   #поля возвращаемые клиенту(берутся из models.py)