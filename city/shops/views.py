import io

from django.shortcuts import render
from django.http import *
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import (City, Street, Shop)
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

        content = JSONRenderer().render(serializer.data)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)

        data['id'] = (Shop.objects.values_list().last())[0] + 1
        data['shop_city_id'] = City.objects.get(city_name=data['shop_city_id']['city_name'])
        data['shop_street_id'] = Street.objects.get(street_name=data['shop_street_id']['street_name'])

        item = Shop.objects.create(

            id=data['id'],

            shop_name=data['shop_name'],

            shop_city_id=data['shop_city_id'],

            shop_street_id=data['shop_street_id'],

            shop_house_id=data['shop_house_id'],

            shop_time_to_open=data['shop_time_to_open'],

            shop_time_to_close=data['shop_time_to_close'], )

        resp_data = {"id": data["id"]}
        return JsonResponse(resp_data, status=status.HTTP_200_OK)

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
