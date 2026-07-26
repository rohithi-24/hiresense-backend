from app.database import SessionLocal
from app import models
from app.utils import hash_password


def seed_admin_user():
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email == "admin@hiresense.com").first()
        if existing:
            print("Admin already exists!")
            return
        admin = models.User(
            name="Admin",
            email="admin@hiresense.com",
            hashed_password=hash_password("admin123"),
            role="admin",
        )
        db.add(admin)
        db.commit()
        print("Admin created: admin@hiresense.com / admin123")
    finally:
        db.close()