from django.db import models


# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=80)


class Street(models.Model):
    street_name = models.CharField(max_length=80)
    street_city_id = models.ForeignKey(City, on_delete=models.CASCADE)


class Shop(models.Model):
    shop_name = models.CharField(max_length=40)
    shop_city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    shop_street_id = models.ForeignKey(Street, on_delete=models.CASCADE)
    shop_house_id = models.IntegerField()
    shop_time_to_open = models.TimeField()
    shop_time_to_close = models.TimeField()
