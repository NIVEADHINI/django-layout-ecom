from django import forms

class OrderCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

