from datetime import datetime

from factory import Faker, LazyFunction, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from app.core.security import get_password_hash
from app.models.user import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)
    username = Sequence(lambda n: f"username{n}")
    full_name = Faker("name")
    email = Sequence(lambda n: f"email{n}@test.com")
    password = get_password_hash("password")
    created_at = LazyFunction(datetime.now)
    updated_at = LazyFunction(datetime.now)
