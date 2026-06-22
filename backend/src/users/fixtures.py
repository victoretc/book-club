import factory
from pytest_factoryboy import register

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


register(UserFactory)
