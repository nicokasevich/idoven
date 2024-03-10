from app.core.security import get_password_hash
from app.models.base import SessionLocal
from app.models.user import User

db = SessionLocal()


def seed():
    user = User(
        username="admin",
        email="example@test.com",
        full_name="Admin",
        role="admin",
        password=get_password_hash("password"),
    )
    db.add(user)
    db.commit()


if __name__ == "__main__":
    seed()
    print("Seeded")
