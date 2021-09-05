from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText


class UserFactory(DjangoModelFactory):
    """Factory for User."""

    username = FuzzyText(length=10)

    class Meta:
        model = User
        django_get_or_create = ('username',)


def test_user():
    """test user."""
    assert UserFactory()
