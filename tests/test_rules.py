from unittest.mock import patch

from django.test import TestCase

from djangocms_fil_permissions.rules import has_site_access
from djangocms_fil_permissions.test_utils.factories import (
    PollFactory,
    SiteFactory,
    UserFactory,
    UserSiteFactory,
)


class RulesTestCase(TestCase):
    def test_has_site_access(self):
        usersite = UserSiteFactory()
        poll = PollFactory(site=usersite.site)

        self.assertTrue(has_site_access(usersite.user, poll))

    def test_has_site_access_no_access(self):
        user = UserFactory()
        site = SiteFactory()
        poll = PollFactory(site=site)

        self.assertFalse(has_site_access(user, poll))

    def test_has_site_access_no_site_relation(self):
        user = UserFactory()
        site = SiteFactory()
        poll = PollFactory(site=site)

        with patch(
            "djangocms_fil_permissions.rules.get_site_for_obj", return_value=None
        ) as get_site_for_obj, patch(
            "djangocms_fil_permissions.rules.user_has_access_to_site"
        ) as user_has_access_to_site:
            self.assertTrue(has_site_access(user, poll))
        get_site_for_obj.assert_called_once_with(poll)
        user_has_access_to_site.assert_not_called()
