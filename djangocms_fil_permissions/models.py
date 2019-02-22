from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models


class UserSite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
