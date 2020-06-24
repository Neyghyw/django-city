from django.db import models


class City(models.Model):
    name = models.CharField(max_length=80)


class Street(models.Model):
    name = models.CharField(max_length=80)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)


class Shop(models.Model):
    name = models.CharField(max_length=40)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    street_id = models.ForeignKey(Street, on_delete=models.CASCADE)
    house_id = models.IntegerField()
    time_to_open = models.TimeField()
    time_to_close = models.TimeField()
