from app.database import SessionLocal, Base, engine
from app import models
from app.utils import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if admin already exists
existing = db.query(models.User).filter(models.User.email == "admin@hiresense.com").first()
if existing:
    print("Admin already exists!")
else:
    admin = models.User(
        name="Admin",
        email="admin@hiresense.com",
        hashed_password=hash_password("admin123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    print("Admin created: admin@hiresense.com / admin123")

db.close()