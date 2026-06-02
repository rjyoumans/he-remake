from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    computer = relationship("Computer", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Computer(Base):
    __tablename__ = "computers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    cpu = Column(Integer, default=1)  # Number of CPU cores
    ram = Column(Integer, default=1024)  # RAM in MB
    storage = Column(Integer, default=100)  # Storage in MB
    internet_speed = Column(Integer, default=1)  # Internet speed in Mbps

    money = Column(Integer, default=0)  # User's money balance
    reputation = Column(Integer, default=0)  # User's reputation score

    user = relationship("User", back_populates="computer")
    ip_addresses = relationship("IPAddress", back_populates="computer", cascade="all, delete-orphan")

class IPAddress(Base):
    __tablename__ = "ip_addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True, nullable=False)
    computer_id = Column(Integer, ForeignKey("computers.id"), nullable=True)

    computer = relationship("Computer", back_populates="ip_addresses")
