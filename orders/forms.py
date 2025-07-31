from django import forms
from orders.models import Order

class OrderForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows' : 3, 'placeholder' : 'адрес доставки'}))
    phone = forms.CharField(max_length=20, required=True)
    payment_method = forms.ChoiceField(choices=[('card', 'Карта'), ('cash', 'Наличные')])

    class Meta:
        model = Order
        # fields = ('shipping_address', 'phone', 'payment_method')
        fields = ['shipping_address', 'phone'] 