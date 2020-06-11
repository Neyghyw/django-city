from django.shortcuts import render
from django.http import *
from .models import City
from .models import Street
from .models import Shop
import datetime
from django.utils import timezone


# Create your views here.

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

    if request.method == 'POST':
        return HttpResponse("<h2>Shop create</h2>")

    elif request.method == 'GET':

        try:
            street = request.GET.get("street", -1)
            city = request.GET.get("city", -1)
            open = request.GET.get("open", -1)
            if open == "1":
                shops = Shop.objects.filter(shop_city_id=city, shop_street_id=street,
                                            shop_time_to_open__lte=timezone.now(),
                                            shop_time_to_close__gte=timezone.now())
                print(type(shops))
            elif open == "0":
                shops = Shop.objects.filter(shop_city_id=city, shop_street_id=street,
                                            shop_time_to_open__gt=timezone.now(),
                                            shop_time_to_close__gt=timezone.now())
            return render(request, "getshops.html", {"shops": shops}, status=200)

        except:
            return HttpResponse("<h2>Status 400</h2>", status=400)
