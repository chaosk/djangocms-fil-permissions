.. djangocms-fil-permissions documentation master file, created by
   sphinx-quickstart on Thu Feb 14 11:45:02 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to djangocms-fil-permissions's documentation!
=====================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Overview
--------

Django CMS FIL Permissions provides a way to restrict admin users
to only access objects related to sites that they have been granted access to.

.. note::

    This addon will only automatically apply site-based permissions
    to the ModelAdmin of registered models.

Installation
------------

Run::

    pip install djangocms-fil-permissions


Add ``djangocms_fil_permissions`` to your project's ``INSTALLED_APPS``.

Add ``djangocms_fil_permissions.permissions.SitePermissionBackend``
to your ``AUTHENTICATION_BACKENDS``:

.. code-block:: python

    AUTHENTICATION_BACKENDS = {
        "djangocms_fil_permissions.permissions.SitePermissionBackend",
        "django.contrib.auth.backends.ModelBackend",
    )

Apply migrations::

    python manage.py migrate

Configuration
-------------

FIL Permissions uses the Django CMS app registration system.
To configure your addon to use FIL Permissions, create a ``cms_config.py`` file
in your addon's folder. The most simple configuration looks like this:

.. code-block:: python

    # polls/models.py
    from django.contrib.sites.models import Site
    from django.db import models

    class Poll(models.Model):
        site = models.ForeignKey(Site, on_delete=models.CASCADE)

.. code-block:: python

    # polls/cms_config.py
    from cms.app_base import CMSAppConfig
    from .models import Poll

    class PollsAppConfig(CMSAppConfig):
        djangocms_fil_permissions_enabled = True

        site_permission_models = {
            Poll: "site",
        }

In this example, ``Poll`` has a ``site`` field, which is a relation to ``Site``
model.

.. note::

    Relation to ``Site`` model can be either a foreign key or a many to many
    field.

:py:class:`CMSAppConfig`

    :py:attr:`~djangocms_fil_permissions_enabled`

    Your ``cms_config.py`` needs to define a single subclass of ``CMSAppConfig``
    with ``djangocms_fil_permissions_enabled = True``. This instructs
    Django CMS to pass your config to FIL Permissions extension.

    :py:attr:`~site_permission_models`

    This attribute allows for registering models
    into per-site permission system.

    It needs to be a dict of the following format: ``{model: site_relation}``.

    .. note::
       ``site_relation`` is a Django-style field lookup (e.g. ``foo__site``)
       to retrieve Site object

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
