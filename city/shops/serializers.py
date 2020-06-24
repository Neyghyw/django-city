from rest_framework import serializers
from .models import (Shop, City, Street)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ['name']


class ShopSerializer(serializers.ModelSerializer):
    city_id = CitySerializer(read_only=False)
    street_id = StreetSerializer(read_only=False)

    class Meta:
        model = Shop
        fields = ['name',
                  'house_id',
                  'time_to_open',
                  'time_to_close',
                  'city_id',
                  'street_id']
