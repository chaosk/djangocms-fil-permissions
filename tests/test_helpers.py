from unittest.mock import MagicMock, Mock, patch

from django.apps import apps
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from rules.contrib.admin import ObjectPermissionsModelAdminMixin

from djangocms_fil_permissions.helpers import (
    _replace_admin_for_model,
    admin_factory,
    get_extension,
    get_sites_for_obj,
    replace_admin_for_model,
    translate_relation,
    user_can_access_any_of_sites,
)
from djangocms_fil_permissions.test_utils.factories import (
    AnswerFactory,
    PizzaFactory,
    PollFactory,
    SiteFactory,
    UserSiteFactory,
)
from djangocms_fil_permissions.test_utils.polls.models import Answer, Poll
from djangocms_fil_permissions.test_utils.restaurants.models import Pizza


class GetExtensionTestCase(TestCase):
    def setUp(self):
        get_extension.cache_clear()

    def tearDown(self):
        get_extension.cache_clear()

    def test_get_extension(self):
        models = ["Foo", "Bar"]
        app_config = Mock(
            spec=[], cms_extension=Mock(spec=[], site_permission_models=models)
        )
        with patch.object(apps, "get_app_config", return_value=app_config):
            self.assertEqual(get_extension(), app_config.cms_extension)

    def test_get_extension_is_cached(self):
        models = ["Foo", "Bar"]
        app_config = Mock(
            spec=[], cms_extension=Mock(spec=[], site_permission_models=models)
        )
        with patch.object(apps, "get_app_config", return_value=app_config):
            get_extension()
        with patch.object(apps, "get_app_config") as mock:
            get_extension()
            mock.assert_not_called()


class HelpersTestCase(TestCase):
    def test_get_sites_for_obj(self):
        poll = PollFactory()
        self.assertEqual(get_sites_for_obj(poll), [poll.site])

    def test_get_sites_for_obj_not_registered_for_site_permissions(self):
        poll = PollFactory()

        registry_mock = MagicMock()
        registry_mock.__getitem__.side_effect = KeyError
        with patch(
            "djangocms_fil_permissions.helpers.get_extension",
            return_value=Mock(site_permission_models=registry_mock),
        ):
            self.assertEqual(get_sites_for_obj(poll), [])
        registry_mock.__getitem__.assert_called_once_with(Poll)

    def test_user_can_access_any_of_sites(self):
        usersite = UserSiteFactory()

        self.assertTrue(user_can_access_any_of_sites(usersite.user, [usersite.site]))

    def test_user_can_access_any_of_sites_partial_overlap(self):
        usersite = UserSiteFactory()
        usersite2 = UserSiteFactory(user=usersite.user)
        site3 = SiteFactory()

        self.assertTrue(
            user_can_access_any_of_sites(usersite.user, [usersite2.site, site3])
        )

    def test_user_can_access_any_of_sites_no_access(self):
        usersite = UserSiteFactory()
        site2 = SiteFactory()

        self.assertFalse(user_can_access_any_of_sites(usersite.user, [site2]))

    def test_admin_factory(self):
        base_class = type("A", (), {})
        mixin = type("B", (), {})
        subclass = admin_factory(base_class, mixin)
        self.assertEqual(subclass.__name__, base_class.__name__)
        self.assertTrue(issubclass(subclass, base_class))
        self.assertTrue(issubclass(subclass, mixin))


class HelpersAdminSiteTestCase(TestCase):
    def setUp(self):
        self.site = admin.AdminSite()

    def test_replace_admin_for_model(self):
        self.site.register(Poll)
        with patch(
            "djangocms_fil_permissions.helpers._replace_admin_for_model"
        ) as mock:
            replace_admin_for_model(Poll, self.site)
        mock.assert_called_once_with(
            self.site._registry[Poll], ObjectPermissionsModelAdminMixin, self.site
        )

    def test_replace_admin_for_model_not_registered(self):
        self.site = admin.AdminSite()
        with patch(
            "djangocms_fil_permissions.helpers._replace_admin_for_model"
        ) as mock:
            replace_admin_for_model(Poll, self.site)
        mock.assert_not_called()

    def test__replace_admin_for_model_already_with_mixin(self):
        mixin = type("Mixin", (), {})
        modeladmin_class = type("ModelAdmin", (admin.ModelAdmin, mixin), {})
        modeladmin = modeladmin_class(Poll, self.site)
        with patch("djangocms_fil_permissions.helpers.admin_factory") as mock:
            _replace_admin_for_model(modeladmin, mixin, self.site)
        mock.assert_not_called()

    def test__replace_admin_for_model(self):
        modeladmin_class = type("ModelAdmin", (admin.ModelAdmin,), {})
        mixin = type("Mixin", (), {})
        self.site.register(Poll, modeladmin_class)
        modeladmin = self.site._registry[Poll]
        _replace_admin_for_model(modeladmin, mixin, self.site)
        new_modeladmin = self.site._registry[Poll]
        self.assertNotEqual(modeladmin, new_modeladmin)
        self.assertTrue(isinstance(new_modeladmin, mixin))


class TranslateRelationTestCase(TestCase):
    def test_not_pointing_to_site(self):
        with self.assertRaises(
            ImproperlyConfigured,
            msg='Relation "poll" does not point to Site model (it targets polls.Poll instead).',
        ):
            translate_relation(Answer, "poll")

    def test_fk(self):
        answer = AnswerFactory()
        getter = translate_relation(Answer, "poll__site")
        self.assertEqual(getter(answer), [answer.poll.site])

    def test_m2m(self):
        sites = SiteFactory.create_batch(3)
        pizza = PizzaFactory(restaurant__sites=sites)
        getter = translate_relation(Pizza, "restaurant__sites")
        self.assertEqual(
            set(site.pk for site in getter(pizza)), set(site.pk for site in sites)
        )
