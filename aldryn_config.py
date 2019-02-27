from aldryn_client import forms


class Form(forms.BaseForm):
    def to_settings(self, data, settings):
        settings["AUTH_USER_MODEL"] = "djangocms_fil_permissions.User"
        authentication_backends = settings.get("AUTHENTICATION_BACKENDS", [])
        authentication_backends.insert(
            0, "djangocms_fil_permissions.permissions.SitePermissionBackend"
        )
        settings["AUTHENTICATION_BACKENDS"] = authentication_backends
        return settings
