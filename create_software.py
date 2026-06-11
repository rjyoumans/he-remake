from app.database import SessionLocal
from app.models import Software


db = SessionLocal()

software_list = [
    {
        "name": "Basic Cracker.crc",
        "version": "1.0",
        "size": 28,
        "software_type": "Cracker",
    },
    {
        "name": "Basic Hasher.hash",
        "version": "1.0",
        "size": 26,
        "software_type": "Hasher",
    },
    {
        "name": "Basic Port Scan.scan",
        "version": "1.0",
        "size": 23,
        "software_type": "Port Scanner",
    },
    {
        "name": "Basic Firewall.fwl",
        "version": "1.0",
        "size": 23,
        "software_type": "Firewall",
    },
    {
        "name": "Basic Hider.hdr",
        "version": "1.0",
        "size": 17,
        "software_type": "Hider",
    },
    {
        "name": "Basic Seeker.skr",
        "version": "1.0",
        "size": 17,
        "software_type": "Seeker",
    },
    {
        "name": "Basic Spam.vspam",
        "version": "1.0",
        "size": 14,
        "software_type": "Spam",
    },
    {
        "name": "Basic Collector.vcol",
        "version": "1.0",
        "size": 16,
        "software_type": "Collector",
    },
    {
        "name": "Basic FTP Exploit.exp",
        "version": "1.0",
        "size": 21,
        "software_type": "FTP Exploit",
    },
    {
        "name": "Basic SSH Exploit.exp",
        "version": "1.0",
        "size": 21,
        "software_type": "SSH Exploit",
    },
]

for software_data in software_list:
    existing = db.query(Software).filter(
        Software.name == software_data["name"]
    ).first()

    if not existing:
        software = Software(**software_data)
        db.add(software)
        print(f"Added {software.name}")
    else:
        print(f"{software_data['name']} already exists")


db.commit()
db.close()

print("Software seeding complete.")