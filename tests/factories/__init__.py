from tests.factories.user import UserFactory

sqlalchemy_factories: list = [
    UserFactory,
]


__all__ = ["UserFactory"]
