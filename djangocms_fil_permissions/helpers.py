from functools import lru_cache

from django.apps import apps
from django.contrib import admin
from django.contrib.sites.models import Site

from rules.contrib.admin import ObjectPermissionsModelAdminMixin


@lru_cache(maxsize=1)
def get_extension():
    app = apps.get_app_config("djangocms_fil_permissions")
    return app.cms_extension


def get_site_for_obj(obj):
    """Returns a Site that's related to the provided object.
    Returns None if object's model is not registered for
    per-site permissions.

    :param obj: A model object
    """
    extension = get_extension()
    try:
        getter = extension.site_permission_models[obj.__class__]
    except KeyError:
        return
    return getter(obj)


def user_has_access_to_site(user, site):
    """Returns True if user is associated with provided site,
    otherwise returns False.

    :param user: User instance
    :param site: Site instance
    """
    return Site.objects.filter(usersite__user=user, pk=site.pk).exists()


def admin_factory(admin_class, mixin):
    """A class factory returning subclass of `mixin` and `admin_class`.

    :param admin_class: Existing admin class
    :param mixin: Mixin class
    :return: A subclass of `mixin` and `admin_class`
    """
    return type(admin_class.__name__, (mixin, admin_class), {})


def _replace_admin_for_model(modeladmin, mixin, admin_site):
    """Replaces existing admin class registered for `modeladmin.model` with
    a subclass that includes `mixin`.

    Doesn't do anything if `modeladmin` is already an instance of
    `mixin`.

    :param model: ModelAdmin instance
    :param mixin: Mixin class
    :param admin_site: AdminSite instance
    """
    if isinstance(modeladmin, mixin):
        return
    new_admin_class = admin_factory(modeladmin.__class__, mixin)
    admin_site.unregister(modeladmin.model)
    admin_site.register(modeladmin.model, new_admin_class)


def replace_admin_for_model(model, admin_site=None):
    """Replace existing admin class registered for `model` with
    a subclass that includes per-object permissions checking.

    :param models: Model class
    :param admin_site: AdminSite instance
    """
    if admin_site is None:
        admin_site = admin.site
    try:
        modeladmin = admin_site._registry[model]
    except KeyError:
        return
    _replace_admin_for_model(modeladmin, ObjectPermissionsModelAdminMixin, admin_site)
