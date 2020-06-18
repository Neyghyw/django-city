
from django.conf.urls import url
from django.urls import path
from shops import views

urlpatterns = [
    path('city/<int:city>/street/', views.Getstreets),
    url('shop/', views.ShopsListView.as_view(), name="shops_list"),
    path('city/', views.Getcities),
]
