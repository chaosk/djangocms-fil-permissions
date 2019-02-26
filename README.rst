====================
djangocms-fil-permissions
====================

Installation
============

Requirements
============

django CMS FIL Permissions requires that you have a django CMS 4.0 (or higher) project already running and set up.


To install
==========

Run::

    pip install djangocms-fil-permissions

Add ``djangocms_fil_permissions`` to your project's ``INSTALLED_APPS``.

Add ``djangocms_fil_permissions.permissions.SitePermissionBackend``
to your ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = {
        "djangocms_fil_permissions.permissions.SitePermissionBackend",
        "django.contrib.auth.backends.ModelBackend",
    )

Apply migrations::

    python manage.py migrate
