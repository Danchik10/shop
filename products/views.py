from django.shortcuts import render, redirect, HttpResponseRedirect
from products.models import Product, ProductsCategory, Basket
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