from django.db import models

# from django.core.cache import cache

from orders.models import Order

class ProductsCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    # @classmethod
    # def get_all_cached(cls):
    #     categories = cache.get('all_categories')
    #     if not categories:
    #         categories = list(cls.objects.all())
    #         cache.set('all_categories', categories, 60*15)
    #     return categories

    # def __str__(self):
    #     return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductsCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.category}"

class Basket(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина: {self.user.email} | Продукт: {self.product.name}"
    
    def sum(self):
        return self.product.price * self.quantity