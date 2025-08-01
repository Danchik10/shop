from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline): #TabularInline - отображает элементы в виде таблицы
    model = OrderItem
    extra = 0       #не показывать пустые формы в Django-админке

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_timestamp', 'total_price', 'status')
    inlines = (OrderItemInline,)       #позволяет редактировать элементы заказа прямо на странице редактирования заказа
