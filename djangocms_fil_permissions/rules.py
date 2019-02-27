import rules

from .helpers import get_site_for_obj, user_has_access_to_site


@rules.predicate
def has_site_access(user, obj):
    site = get_site_for_obj(obj)
    if site is None:
        return True
    return user_has_access_to_site(user, site)
