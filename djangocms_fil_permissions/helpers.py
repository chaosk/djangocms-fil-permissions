from functools import lru_cache, reduce

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.utils import get_fields_from_path
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet

from rules.contrib.admin import ObjectPermissionsModelAdminMixin


@lru_cache(maxsize=1)
def get_extension():
    app = apps.get_app_config("djangocms_fil_permissions")
    return app.cms_extension


def get_sites_for_obj(obj):
    """Returns a list of Site objects that are related to the provided object.
    Returns empty list if object's model is not registered for
    per-site permissions.

    :param obj: A model object
    """
    extension = get_extension()
    try:
        getter = extension.site_permission_models[obj.__class__]
    except KeyError:
        return []
    return getter(obj)


def user_can_access_any_of_sites(user, sites):
    """Returns True if user is associated with any of the provided sites,
    otherwise returns False.

    :param user: User instance
    :param site: List or a queryset of sites
    """
    if not isinstance(sites, QuerySet):
        sites = [site.pk for site in sites]
    return Site.objects.filter(usersite__user=user, pk__in=sites).exists()


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


def translate_relation(model, relation):
    """Transforms Django-style related field lookup (foo__bar)
    into attrgetter instance that can be called with an object
    to retrieve the object at the end of defined relation chain.

    :param relation: Django-style field lookup
    """
    fields = get_fields_from_path(model, relation)
    last_field = fields[-1]
    if not issubclass(last_field.related_model, Site):
        raise ImproperlyConfigured(
            'Relation "{}" does not point to Site model (it targets {} instead).'.format(
                relation,
                "{}.{}".format(
                    last_field.related_model._meta.app_label,
                    last_field.related_model.__name__,
                ),
            )
        )

    def get_next_field(obj, field):
        return getattr(obj, field.name)

    def inner(obj):
        obj = reduce(get_next_field, fields, obj)
        if last_field.many_to_many:
            return obj.all()
        return [obj]

    return inner
