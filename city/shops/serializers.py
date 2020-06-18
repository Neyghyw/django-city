from rest_framework import serializers
from .models import (Shop, City, Street)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ['street_name']


class ShopSerializer(serializers.ModelSerializer):
    shop_city_id = CitySerializer(read_only=False)
    shop_street_id = StreetSerializer(read_only=False)

    class Meta:
        model = Shop
        fields = ['shop_name',
                  'shop_house_id',
                  'shop_time_to_open',
                  'shop_time_to_close',
                  'shop_city_id',
                  'shop_street_id']
