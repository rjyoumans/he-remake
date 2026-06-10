from app.database import SessionLocal
from app.models import Software

db = SessionLocal()

existing = db.query(Software).filter(Software.name == "Basic Cracker.crc").first()

if not existing:
    basic_cracker = Software(
        name="Basic Cracker.crc",
        version="1.0",
        size=26,
        software_type="Cracker"
    )

    db.add(basic_cracker)
    db.commit()

    print("Basic Cracker.crc added to database.")
else:
    print("Basic Cracker.crc already exists in database.")  

db.close()