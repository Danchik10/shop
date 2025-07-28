from django.shortcuts import render, redirect, HttpResponseRedirect
from products.models import Product, ProductsCategory, Basket
from django.contrib.auth.decorators import login_required

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
        'products' : products,
    }
    return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

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
    basket.delete()
    # return render('users:profile')
    return HttpResponseRedirect(request.META['HTTP_REFERER']) 