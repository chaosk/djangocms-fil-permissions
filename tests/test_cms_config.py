from operator import attrgetter
from unittest.mock import Mock, patch

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from djangocms_fil_permissions import cms_config
from djangocms_fil_permissions.test_utils.polls.models import Answer, Poll


class CMSConfigTestCase(TestCase):
    def test_int_site_permission_models_cms_config_parameter(self):
        """CMS config with int as site_permission_models as it expects
        a dict"""
        extension = cms_config.PermissionsCMSExtension()
        mocked_cms_config = Mock(
            spec=[],
            djangocms_fil_permissions_enabled=True,
            site_permission_models=23234,
            app_config=Mock(label="blah_cms_config"),
        )

        with self.assertRaises(ImproperlyConfigured):
            extension.configure_app(mocked_cms_config)

    def test_valid_cms_config_parameter(self):
        """CMS config with valid configuration"""
        extension = cms_config.PermissionsCMSExtension()
        mocked_cms_config = Mock(
            spec=[],
            djangocms_fil_permissions_enabled=True,
            site_permission_models={Poll: "site"},
            app_config=Mock(label="blah_cms_config"),
        )

        with patch.object(extension, "translate_relation", side_effect=lambda v: v):
            extension.configure_app(mocked_cms_config)

        self.assertTrue(Answer not in extension.site_permission_models.keys())
        self.assertTrue(Poll in extension.site_permission_models.keys())
        self.assertEqual(extension.site_permission_models[Poll], "site")

    def test_no_site_permission_models(self):
        extension = cms_config.PermissionsCMSExtension()
        mocked_cms_config = Mock(
            spec=[],
            djangocms_fil_permissions_enabled=True,
            app_config=Mock(label="blah_cms_config"),
        )

        with patch.object(extension, "configure_models") as configure_models:
            extension.configure_app(mocked_cms_config)
        configure_models.assert_not_called()

    def test_translate_relation(self):
        extension = cms_config.PermissionsCMSExtension()
        getter = extension.translate_relation("foo__bar")
        mock = Mock()
        self.assertEqual(getter(mock), mock.foo.bar)

    def test_register_model(self):
        extension = cms_config.PermissionsCMSExtension()
        with patch.object(extension, "translate_relation") as translate_relation:
            extension.register_model(Poll, "foo__site")
        translate_relation.assert_called_once_with("foo__site")
        self.assertEqual(
            extension.site_permission_models[Poll], translate_relation.return_value
        )

    def test_patch_admin(self):
        extension = cms_config.PermissionsCMSExtension()
        with patch(
            "djangocms_fil_permissions.cms_config.replace_admin_for_model"
        ) as mock:
            extension.patch_admin(Poll)
        mock.assert_called_once_with(Poll)


class IntegrationTestCase(TestCase):
    def test_config_with_multiple_apps(self):
        site_permission_models = apps.get_app_config(
            "djangocms_fil_permissions"
        ).cms_extension.site_permission_models
        expected_models = {Poll: attrgetter("site"), Answer: attrgetter("poll.site")}

        self.assertCountEqual(site_permission_models.keys(), expected_models)
