from django.contrib.sites.models import Site
from django.db import models


class Restaurant(models.Model):
    text = models.CharField(max_length=255)
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.text


class Pizza(models.Model):
    text = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
