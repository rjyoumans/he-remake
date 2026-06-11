from app.database import SessionLocal
from app.models import Server

db = SessionLocal()

existing = db.query(Server).filter(Server.ip_address == "237.209.240.197").first()

if not existing:
    download_center = Server(
        ip_address="237.209.240.197",
        name="Download Center",
        description=(
            "Welcome to the Download Center!\n\n"
            "Download whatever you need. Unlimited bandwidth!\n\n"
            "Username: download\n"
            "Password: download"
        ),
        server_type="npc",
        username="download",
        password="download",
    )

    db.add(download_center)
    db.commit()
    print("Download Center created")
else:
    print("Download Center already exists")

db.close()