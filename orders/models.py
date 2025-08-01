from django.db import models
from users.models import User
# from products.models import Product


#заказ "в целом"
class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50, choices=[('card', 'Карта'), ('cash', 'Наличные')], default='card')
    status = models.CharField(max_length=50, default='pending')

#товары, которые будут в заказе
class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to='products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Order #{self.order.id})"