from django import forms

class ShopsFilterForm(forms.form):
    street = forms.IntegerField(label="Улица")
    city = forms.IntegerField(label="Город")
    open = forms.IntegerField(label="оз")