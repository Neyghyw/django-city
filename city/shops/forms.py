from django import forms


class ShopsFilterForm(forms.Form):
    name = forms.CharField()
    city_id = forms.IntegerField()
    street_id = forms.IntegerField()
    house_id = forms.IntegerField()
    time_to_open = forms.TimeField()
    time_to_close = forms.TimeField()
