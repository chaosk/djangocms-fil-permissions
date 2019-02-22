from django.core.exceptions import PermissionDenied

from rules.rulesets import RuleSet

from .rules import has_site_access


site_permissions = RuleSet()
site_permissions.add_rule("site_perm", has_site_access)


class SitePermissionBackend(object):
    """Authentication backend that checks row-level permissions granted
    on site-level.
    """

    def authenticate(self, request, **credentials):
        return None

    def has_perm(self, user, perm, obj=None):
        """Checks if ``user` belongs to a site associated with ``obj``.

        Denies access if ``obj`` is registered for site-level permissions
        and ``user`` does not belong to the same site as ``obj``.

        In any other case (``user`` passed the test or ``obj``
        is not registered for site-level permissions,
        no ``obj`` is passed), permission checking continues to the
        next authentication backend.

        :param user: User instance
        :param perm: Permission codename
        :param obj: Object checked against
        """
        if not site_permissions.test_rule("site_perm", user, obj):
            raise PermissionDenied()
        return None

    def has_module_perms(self, user, app_label):
        return None
