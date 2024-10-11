from importlib import import_module

from django.conf import settings

import factory
import factory.fuzzy
from sessionprofile.models import SessionProfile


class SessionProfileFactory(factory.django.DjangoModelFactory):

    session_key = factory.fuzzy.FuzzyText(length=40)

    class Meta:
        model = SessionProfile

    @classmethod
    def create(cls, **kwargs):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

        instance = super().create(**kwargs)
        SessionStore(instance.session_key).save(True)

        return instance
