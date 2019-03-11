from cms.app_base import CMSAppConfig

from .models import Pizza, Restaurant


class RestaurantsCMSAppConfig(CMSAppConfig):
    djangocms_fil_permissions_enabled = True
    site_permission_models = {Restaurant: "sites", Pizza: "restaurant__sites"}
