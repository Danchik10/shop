from django.shortcuts import render
from products.models import Product, ProductsCategory

def index(request):
    context = {'title' : 'Store'}

    return render(request, 'products/index.html', context)

def products(request, category_id = None):
    if category_id:
        category = ProductsCategory.objects.get(id = category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    context = {
        'title' : 'Store - Каталог',
        'categories' : ProductsCategory.objects.all(),
        'products' : products
    }
    return render(request, 'products/products.html', context)