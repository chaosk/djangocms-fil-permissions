from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PermissionsConfig(AppConfig):
    name = "djangocms_fil_permissions"
    verbose_name = _("django CMS FIL Permissions")
