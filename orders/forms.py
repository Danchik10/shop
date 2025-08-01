from django import forms
from orders.models import Order

class OrderForm(forms.ModelForm):
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows' : 3, 'placeholder' : 'адрес доставки'}))
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Order
        fields = ('shipping_address', 'phone', 'payment_method')