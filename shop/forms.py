from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "phone": forms.TextInput(attrs={"placeholder": "+996 ..."}),
            "address": forms.TextInput(attrs={"placeholder": "Адрес доставки"}),
            "comment": forms.Textarea(attrs={"placeholder": "Комментарий к заказу", "rows": 4}),
        }
