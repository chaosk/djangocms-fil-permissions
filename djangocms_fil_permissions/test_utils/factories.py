from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import factory
from factory.fuzzy import FuzzyText

from ..models import UserSite
from .polls.models import Answer, Poll


class SiteFactory(factory.django.DjangoModelFactory):
    domain = FuzzyText(length=12)

    class Meta:
        model = Site


class PollFactory(factory.django.DjangoModelFactory):
    text = FuzzyText(length=12)
    site = factory.SubFactory(SiteFactory)

    class Meta:
        model = Poll


class AnswerFactory(factory.django.DjangoModelFactory):
    text = FuzzyText(length=12)
    poll = factory.SubFactory(PollFactory)

    class Meta:
        model = Answer


class UserFactory(factory.django.DjangoModelFactory):
    username = FuzzyText(length=12)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda u: "%s.%s@example.com" % (u.first_name.lower(), u.last_name.lower())
    )

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class UserSiteFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    site = factory.SubFactory(SiteFactory)

    class Meta:
        model = UserSite
