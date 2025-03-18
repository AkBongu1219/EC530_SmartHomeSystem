# schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

# --------------------------
# User Schemas
# --------------------------

class UserCreate(BaseModel):
    name: str
    username: str
    phone_number: str
    email: str
    privilege: str  # e.g., "admin", "regular", "guest"

class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    phone_number: str
    email: str
    privilege: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --------------------------
# House Schemas
# --------------------------

class HouseCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    owner_ids: List[str]
    occupant_count: int

class HouseResponse(BaseModel):
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    owner_ids: List[str]
    occupant_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --------------------------
# Room Schemas
# --------------------------

class RoomCreate(BaseModel):
    name: str
    floor: int
    size: float
    house_id: str
    type: str  # e.g., "bedroom", "kitchen", etc.

class RoomResponse(BaseModel):
    id: str
    name: str
    floor: int
    size: float
    house_id: str
    type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# --------------------------
# Device Schemas
# --------------------------

class DeviceCreate(BaseModel):
    type: str  # e.g., "light", "thermostat", etc.
    name: str
    room_id: str
    settings: Optional[Dict] = Field(default_factory=dict)

class DeviceResponse(BaseModel):
    id: str
    type: str
    name: str
    room_id: str
    settings: Dict
    status: bool
    last_data: Dict
    last_updated: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True