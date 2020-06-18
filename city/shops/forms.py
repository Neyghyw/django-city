from django import forms


class ShopsFilterForm(forms.Form):
    shop_name = forms.CharField()
    shop_city_id = forms.IntegerField()
    shop_street_id = forms.IntegerField()
    shop_house_id = forms.IntegerField()
    shop_time_to_open = forms.TimeField()
    shop_time_to_close = forms.TimeField()
