from django.shortcuts import render, redirect
from orders.forms import OrderForm
from orders.models import Order, OrderItem
from products.models import Basket

# Create your views here.
def order(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    #Получает все товары из корзины текущего пользователя
    basket_items = Basket.objects.filter(user=request.user)

    #Если корзина пуста - перенаправляет на главную страницу
    if not basket_items.exists():
        return redirect('products:index')

    total_price = sum(item.product.price*item.quantity for item in basket_items)
    if request.method == 'POST':        #при отправке заказа
        form = OrderForm(request.POST)      #Создаёт экземпляр формы с переданными данными
        if form.is_valid():
            # Создаём и сохраняем заказ
            try:
                order=form.save(commit=False)   #commit=False - создаёт объект Order, но не сохраняет в БД
                order.user = request.user       #Привязывает пользователя
                order.total_price = total_price  #Устанавливает общую сумму
                order.status = 'pending'
                order.save()                    #Сохраняет заказ в БД
                #Товары из корзины переносятся в заказ.
                for item in basket_items:
                    OrderItem.objects.create(
                        order=order,        #Для каждого товара в корзине создаёт запись OrderItem
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity)
                basket_items.delete()
                return redirect('products:index')       #Перенаправляет на главную страницу после успешного оформления
            except Exception as e:
                print(f"Error saving order: {e}")

    else:                                                       #При открытии формы об оформлении заказа(первое открытие страницы)
        form=OrderForm(initial={'payment_method' : 'card'})     

    context = {
        'form' : form,
        'basket' : basket_items,
        'total_price' : total_price,
    }
    return render(request, 'orders/order.html', context)