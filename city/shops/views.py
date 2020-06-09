from django.shortcuts import render
from django.http import *
from .models import City
from .models import Street
from .models import Shop
import datetime
from django.utils import timezone


# Create your views here.

def Getcities(request):
    cities = City.objects.all()
    return render(request, "index.html", {"cities": cities})


def Getstreets(request, city):
    streets = Street.objects.filter(street_city_id=city)
    return render(request, "streets.html", {"streets": streets})


def Shopcreate(request):
    return HttpResponseBadRequest("<h2>Shop create</h2>")


def Getshop(request):
    street = request.GET.get("street")
    city = request.GET.get("city")
    open = request.GET.get("open")
    shops = Shop.objects.filter(shop_city_id=city, shop_street_id=street, shop_time_to_open__lte=timezone.now(),
                                shop_time_to_close__gte=timezone.now())
    return render(request, "getshops.html", {"shops": shops})
