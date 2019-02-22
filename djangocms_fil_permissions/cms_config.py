from collections.abc import Mapping
from operator import attrgetter

from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppExtension

from .helpers import replace_admin_for_model


class PermissionsCMSExtension(CMSAppExtension):
    def __init__(self):
        self.site_permission_models = {}

    def translate_relation(self, relation):
        """Transforms Django-style related field lookup (foo__bar)
        into attrgetter instance that can be called with an object
        to receive the object at the end of defined relation chain.

        :param relation: Django-style field lookup
        """
        fields = relation.split("__")
        return attrgetter(".".join(fields))

    def register_model(self, model, site_relation):
        """Registers model for per-site permission system.

        :param model: Model class
        :param site_relation: Related field lookup pointing to a FK to
                              a Site from the provided model
        """
        self.site_permission_models[model] = self.translate_relation(site_relation)

    def patch_admin(self, model):
        """Patches the modeladmin for provided `model` to include
        per-object permission checking.

        :param model: Model class
        """
        replace_admin_for_model(model)

    def configure_models(self, definitions):
        """Registers models for per-site permission system and amends
        its admin to respect per-object permissions.

        :param definitions: A mapping of {model: site_relation}.

        site_relation can be a related field lookup (e.g. foo__site)
        and must point to a foreign key to Site used
        in permission checking

        Example:
        {Article: "site"} enables per-site permissions on Article model
        """
        for model, site_relation in definitions.items():
            self.register_model(model, site_relation)
            self.patch_admin(model)

    def configure_app(self, cms_config):
        site_permission_models = getattr(cms_config, "site_permission_models", None)
        if site_permission_models is not None:
            if isinstance(site_permission_models, Mapping):
                self.configure_models(site_permission_models)
            else:
                raise ImproperlyConfigured(
                    "Per-site permission model configuration must be an Iterable instance"
                )
