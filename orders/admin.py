from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_timestamp', 'total_price', 'status')
    inlines = (OrderItemInline,)
