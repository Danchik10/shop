from rest_framework import generics, viewsets 
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAdminOrReadOnly
from .models import Product, ProductsCategory, Basket
from .serializers import ProductSerializer, BasketSerializer
from rest_framework.views import APIView   #главный класс DRF, связывает запрос с его методом
from rest_framework.response import Response
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# from django.views.decorators.cache import cache_page

def index(request):
    context = {'title' : 'Store'}

    return render(request, 'products/index.html', context)


# @cache_page(60* 15) # Кэшируем на 15 минут
def products(request, category_id = None, page_number=1):
    if category_id:         #если user нажимает на определенную категорию, выводятся только товары из выбранной категории
        category = ProductsCategory.objects.get(id = category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 3)
    products_paginator = paginator.page(page_number)

    context = {
        'title' : 'Store - Каталог',
        'categories' : ProductsCategory.objects.all(),
        'products' : products_paginator,
    }
    return render(request, 'products/products.html', context)

#--------------------------------API-------------------------------#
class ProductAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)   #IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, IsAuthenticated
#   authentication_classes = (TokenAuthentication,)

#action позволяет внутри данного(товары) представления добавить новый маршрут(например категории)
    @action(methods=['get'], detail=True)  #detail=True означает что получаем одну категорию и ссылка выглядит так: api/products/1/category/
    def category(self, request, pk=None):
        categories = ProductsCategory.objects.get(pk=pk)
        #return Response({'category' : [c.name for c in category]})
        return Response({'category' : categories.name})
#--------------------------------API-------------------------------#

@login_required              #позволяет не зарегистрированному пользователю добавить товар в корзину
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)                                #кладем продукт в корзину
    baskets = Basket.objects.filter(user=request.user, product=product)         #берем все корзины пользователя с определенным продуктом

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity +=1
        basket.save()
    # return redirect('products:index')
    return HttpResponseRedirect(request.META['HTTP_REFERER']) 

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    if basket.quantity>1:
        basket.quantity -=1
        basket.save()
    else:
        basket.delete()
    # return render('users:profile')
    return HttpResponseRedirect(request.META['HTTP_REFERER']) 

#--------------------------------API-------------------------------#
class BasketAPIView(viewsets.ViewSet):
    # queryset = Basket.objects.all()
    # serializer_class = BasketSerializer
    # permission_classes = (IsAuthenticated,)  #если не атворизован, то нельзя ни читать, ни исправлять

    #маршрут для добавления товара
    #api/basket/basket_add/id
    @action(methods=['post'], detail=False, url_path='basket_add/(?P<product_id>[^/.]+)')
    def basket_add(self, request, product_id=None):
        try:
            product = Product.objects.get(id=product_id)
            baskets = Basket.objects.filter(user=request.user, product=product)
            if not baskets.exists():
                Basket.objects.create(user=request.user, product=product, quantity=1)
            else:
                basket = baskets.first()
                basket.quantity +=1
                basket.save()
            return Response({'status' : 'Товар добавлен'})
        except Product.DoesNotExist:
            return Response({'error' : 'Товар не найден'})

    #маршрут для удаления товара
    #api/basket/pk(id=43)/basket_remove/
    @action(methods=['post'], detail=True)
    def basket_remove(self, request, pk=None):
        basket = self.get_object()
        if basket.quantity>1:
            basket.quantity -=1
            basket.save()
        else:
            basket.delete()
        return Response({'status' : 'Товар удалён'})