# models.py
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, JSON
from sqlalchemy.sql import func
import uuid
from shs_api.database import Base

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    privilege = Column(String, nullable=False)  # Stored as string (e.g., "admin", "regular", "guest")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# House model
class House(Base):
    __tablename__ = "houses"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    # Owner IDs stored as a JSON array (list of strings)
    owner_ids = Column(JSON, nullable=False)
    occupant_count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Room model
class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    floor = Column(Integer, nullable=False)
    size = Column(Float, nullable=False)  
    house_id = Column(String, nullable=False)  
    type = Column(String, nullable=False)  # Room type stored as string (e.g., "bedroom", "kitchen")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Device model
class Device(Base):
    __tablename__ = "devices"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)  # Device type as string (e.g., "light", "thermostat")
    name = Column(String, nullable=False)
    room_id = Column(String, nullable=False)  
    settings = Column(JSON, nullable=False, default=dict)  # Device settings stored as JSON
    status = Column(Boolean, nullable=False, default=False)
    last_data = Column(JSON, nullable=False, default=dict)  # Stores the last received data from the device
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())