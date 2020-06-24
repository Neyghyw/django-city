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
    try:
        cities = City.objects.all()
        return render(request, "index.html", {"cities": cities}, status=200)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def Getstreets(request, city) -> HttpResponse:
    try:
        streets = Street.objects.filter(city_id=city)
        return render(request, "streets.html", {"streets": streets}, status=200)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


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

        data['city_id'] = City.objects.get(name=data['city_id']['name'])
        data['street_id'] = Street.objects.get(name=data['street_id']['name'])

        item = Shop.objects.create(
            name=data['name'],
            city_id=data['city_id'],
            street_id=data['street_id'],
            house_id=data['house_id'],
            time_to_open=data['time_to_open'],
            time_to_close=data['time_to_close'], )

        resp_data = {"id": (Shop.objects.values_list().last())[0]}
        return JsonResponse(resp_data, status=status.HTTP_200_OK)

    def get_queryset(self):

        queryset = Shop.objects.all()
        street = self.request.query_params.get('street', None)
        city = self.request.query_params.get('city', None)
        worked = self.request.query_params.get('open', None)

        if street is not None:
            queryset = queryset.filter(street_id=street)
        if city is not None:
            queryset = queryset.filter(city_id=city)
        if worked is not None:
            if worked == "1":
                queryset = queryset.filter(
                    time_to_open__lte=timezone.now(),
                    time_to_close__gte=timezone.now())
            elif worked == "0":
                queryset = queryset.filter(
                    time_to_open__gt=timezone.now(),
                    time_to_close__gt=timezone.now())
        return queryset
