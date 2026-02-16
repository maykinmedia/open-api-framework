import factory.fuzzy
from factory.helpers import post_generation
from sessionprofile.models import SessionProfile

from open_api_framework.utils import get_session_store


class SessionProfileFactory(factory.django.DjangoModelFactory[SessionProfile]):
    session_key = factory.fuzzy.FuzzyText(length=40)

    class Meta:  # pyright: ignore
        model = SessionProfile

    @post_generation
    def session(self, create, extracted, **kwargs):
        SessionStore = get_session_store()
        SessionStore(self.session_key).save(True)  # pyright: ignore
