from django.shortcuts import render, redirect
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from products.models import Basket

# Create your views here.
def order(request):
    basket = Basket.objects.filter(user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order=form.save()
            order.user = request.user
            order.save()
            #Товары из Basket переносятся в OrderItem.
            for item in basket:
                 OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            basket.delete()

            # return render(request, 'orders/order_success.html', {'order' : order})

    else:
        form=OrderForm()

    context = {
        'form' : form,
        'basket' : basket,
    }
    return render(request, 'orders/order.html', context)