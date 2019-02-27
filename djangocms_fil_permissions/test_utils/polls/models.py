from django.contrib.sites.models import Site
from django.db import models


class Poll(models.Model):
    text = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
