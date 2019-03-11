import rules

from .helpers import get_sites_for_obj, user_can_access_any_of_sites


@rules.predicate
def has_site_access(user, obj):
    sites = get_sites_for_obj(obj)
    if not sites:
        return True
    return user_can_access_any_of_sites(user, sites)
