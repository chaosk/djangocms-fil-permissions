from cms.app_base import CMSAppConfig

from .models import Answer, Poll


class PollsCMSAppConfig(CMSAppConfig):
    djangocms_fil_permissions_enabled = True
    site_permission_models = {Poll: "site", Answer: "poll__site"}
