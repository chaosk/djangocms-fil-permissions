HELPER_SETTINGS = {
    "INSTALLED_APPS": [
        "rules",
        "djangocms_fil_permissions",
        "djangocms_fil_permissions.test_utils.polls",
        "djangocms_fil_permissions.test_utils.restaurants",
    ],
    "MIGRATION_MODULES": {
        "auth": None,
        "cms": None,
        "menus": None,
        "sites": None,
        "djangocms_fil_permissions": None,
        "djangocms_fil_permissions.test_utils.polls": None,
        "djangocms_fil_permissions.test_utils.restaurants": None,
    },
    "AUTHENTICATION_BACKENDS": (
        "djangocms_fil_permissions.permissions.SitePermissionBackend",
        "django.contrib.auth.backends.ModelBackend",
    ),
}


def run():
    from djangocms_helper import runner

    runner.cms("djangocms_fil_permissions", extra_args=[])


if __name__ == "__main__":
    run()
