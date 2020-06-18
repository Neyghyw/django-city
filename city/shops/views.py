from django.shortcuts import render
from django.http import *
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (City, Street, Shop)
from .forms import ShopsFilterForm
from .serializers import ShopSerializer


def Getcities(request) -> HttpResponse:
    cities = City.objects.all()
    return render(request, "index.html", {"cities": cities}, status=200)


def Getstreets(request, city) -> HttpResponse:
    streets = Street.objects.filter(street_city_id=city)
    return render(request, "streets.html", {"streets": streets}, status=200)


class ShopsListView(generics.ListCreateAPIView):
    serializer_class = ShopSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item = Shop.objects.create(

            id=(Shop.objects.values_list().last())[0] + 1,

            shop_name=serializer.data['shop_name'],

            shop_city_id=City.objects.get(city_name=serializer.data['shop_city_id']['city_name']),

            shop_street_id=Street.objects.get(street_name=serializer.data['shop_street_id']['street_name']),

            shop_house_id=serializer.data['shop_house_id'],

            shop_time_to_open=serializer.data['shop_time_to_open'],

            shop_time_to_close=serializer.data['shop_time_to_close'], )

        result = ShopSerializer(item)
        return Response(result.data, status=status.HTTP_200_OK)

    def get_queryset(self):

        queryset = Shop.objects.all()
        street = self.request.query_params.get('street', None)
        city = self.request.query_params.get('city', None)
        open = self.request.query_params.get('open', None)

        if street is not None:
            queryset = queryset.filter(shop_street_id=street)
        if city is not None:
            queryset = queryset.filter(shop_city_id=city)
        if open is not None:
            if open == "1":
                queryset = queryset.filter(
                    shop_time_to_open__lte=timezone.now(),
                    shop_time_to_close__gte=timezone.now())
            elif open == "0":
                queryset = queryset.filter(
                    shop_time_to_open__gt=timezone.now(),
                    shop_time_to_close__gt=timezone.now())
        return queryset
