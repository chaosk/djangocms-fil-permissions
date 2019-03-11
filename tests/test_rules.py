from abc import ABCMeta, abstractmethod
from unittest.mock import patch

from django.test import TestCase

from djangocms_fil_permissions.rules import has_site_access
from djangocms_fil_permissions.test_utils.factories import (
    PollFactory,
    RestaurantFactory,
    SiteFactory,
    UserFactory,
    UserSiteFactory,
)


class BaseRulesTests(metaclass=ABCMeta):
    @abstractmethod
    def factory(self, site):
        pass

    def test_has_site_access(self):
        usersite = UserSiteFactory()
        obj = self.factory(site=usersite.site)

        self.assertTrue(has_site_access(usersite.user, obj))

    def test_has_site_access_no_access(self):
        user = UserFactory()
        site = SiteFactory()
        obj = self.factory(site=site)

        self.assertFalse(has_site_access(user, obj))

    def test_has_site_access_no_site_relation(self):
        user = UserFactory()
        site = SiteFactory()
        obj = self.factory(site=site)

        with patch(
            "djangocms_fil_permissions.rules.get_sites_for_obj", return_value=None
        ) as get_sites_for_obj, patch(
            "djangocms_fil_permissions.rules.user_can_access_any_of_sites"
        ) as user_can_access_any_of_sites:
            self.assertTrue(has_site_access(user, obj))
        get_sites_for_obj.assert_called_once_with(obj)
        user_can_access_any_of_sites.assert_not_called()


class FKRulesTestCase(BaseRulesTests, TestCase):
    def factory(self, site):
        return PollFactory(site=site)


class M2MRulesTestCase(BaseRulesTests, TestCase):
    def factory(self, site):
        return RestaurantFactory(sites=[site])
