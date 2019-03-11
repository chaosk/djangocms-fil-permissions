from abc import ABCMeta, abstractmethod
from unittest.mock import MagicMock, Mock, patch

from django.core.exceptions import PermissionDenied
from django.test import TestCase

from djangocms_fil_permissions.permissions import SitePermissionBackend
from djangocms_fil_permissions.test_utils.factories import (
    PollFactory,
    RestaurantFactory,
    SiteFactory,
    UserFactory,
    UserSiteFactory,
)


class SmokePermissionsTestCase(TestCase):
    def test_authenticate(self):
        self.assertIsNone(SitePermissionBackend().authenticate(request=None))

    def test_has_module_perms(self):
        user = UserFactory()
        self.assertIsNone(SitePermissionBackend().has_module_perms(user, "polls"))


class BasePermissionsTests(metaclass=ABCMeta):
    @property
    @abstractmethod
    def change_permission(self, site):
        pass

    @abstractmethod
    def factory(self, site):
        pass

    def test_has_perm(self):
        usersite = UserSiteFactory()
        obj = self.factory(site=usersite.site)
        self.assertIsNone(
            SitePermissionBackend().has_perm(usersite.user, self.change_permission, obj)
        )

    def test_has_perm_no_site_access(self):
        usersite = UserSiteFactory()
        site2 = SiteFactory()
        obj = self.factory(site=site2)
        with self.assertRaises(PermissionDenied):
            SitePermissionBackend().has_perm(usersite.user, self.change_permission, obj)

    def test_has_perm_not_registered_for_site_permissions(self):
        usersite = UserSiteFactory()
        site2 = SiteFactory()
        obj = self.factory(site=site2)

        registry_mock = MagicMock()
        registry_mock.__getitem__.side_effect = KeyError
        with patch(
            "djangocms_fil_permissions.helpers.get_extension",
            return_value=Mock(site_permission_models=registry_mock),
        ):
            self.assertIsNone(
                SitePermissionBackend().has_perm(
                    usersite.user, self.change_permission, obj
                )
            )

    def test_has_perm_no_obj_passed(self):
        user = UserFactory()
        self.assertIsNone(SitePermissionBackend().has_perm(user, "polls.change_poll"))


class FKPermissionsTestCase(BasePermissionsTests, TestCase):
    change_permission = "polls.change_poll"

    def factory(self, site):
        return PollFactory(site=site)


class M2MRulesTestCase(BasePermissionsTests, TestCase):
    change_permission = "restaurants.change_restaurant"

    def factory(self, site):
        return RestaurantFactory(sites=[site])
