from django.shortcuts import render
from django.http import *
from django.utils import timezone

import datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (City, Street, Shop)
from .forms import ShopsFilterForm
from .serializers import ShopSerializer


def Getcities(request) -> HttpResponse:
    try:
        cities = City.objects.all()
        return render(request, "index.html", {"cities": cities}, status=200)

    except:
        return HttpResponse("<h2>Status 400</h2>", status=400)


def Getstreets(request, city) -> HttpResponse:
    try:
        streets = Street.objects.filter(street_city_id=city)
        return render(request, "streets.html", {"streets": streets}, status=200)
    except:
        return HttpResponse("<h2>Status 400</h2>", status=400)


def Shops(request) -> HttpResponse:
    form = ShopsFilterForm()
    if request.method == 'POST':
        ShopsListView.as_view()

    elif request.method == 'GET':

        try:
            shops = Shop()
            street = request.GET.get("street", -1)
            city = request.GET.get("city", -1)
            open = request.GET.get("open", -1)
            if open == "1":
                shops = Shop.objects.filter(shop_city_id=city, shop_street_id=street,
                                            shop_time_to_open__lte=timezone.now(),
                                            shop_time_to_close__gte=timezone.now())
            elif open == "0":
                shops = Shop.objects.filter(shop_city_id=city, shop_street_id=street,
                                            shop_time_to_open__gt=timezone.now(),
                                            shop_time_to_close__gt=timezone.now())
            return render(request, "getshops.html", {"shops": shops, "form": form}, status=200)

        except:
            return HttpResponse("<h2>Status 400</h2>", status=400)


class ShopsListView(APIView):
    def get(self, request):
        shops = Shop.objects.all()
        user = self.request.user
        data = ShopSerializer(Shop.objects.filter(), many=True).data
        return Response(data)

