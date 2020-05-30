from django.shortcuts import render
from django.http import *
# Create your views here.

def Getcities(request):
    return HttpResponseBadRequest("<h2>All cities</h2>")

def Getstreets(request, city):
    output = "<h2>All streets of {0}</h2>".format(city)
    return HttpResponse(output)

def Shopcreate(request):
    return HttpResponseBadRequest("<h2>Shop create</h2>")

def Getshop(request):
    street = request.GET.get("street", -1)
    city = request.GET.get("city", 1)
    open = request.GET.get("open", 0)
    output = "<h2>Street id:{0}  city id:{1} open:{2}</h2>".format(street, city, open)
    return HttpResponse(output)