from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import uuid

# Exception classes 
class SmartHomeError(Exception):
    """Base exception class for Smart Home System"""
    pass

class HouseError(SmartHomeError):
    """Exception raised for house-related errors"""
    pass

class UserError(SmartHomeError):
    """Exception raised for user-related errors"""
    pass

class RoomError(SmartHomeError):
    """Exception raised for room-related errors"""
    pass

class DeviceError(SmartHomeError):
    """Exception raised for device-related errors"""
    pass

# System enums for type safety
class UserPrivilege(Enum):
    """Defines user access levels in the system"""
    ADMIN = "admin"
    REGULAR = "regular"
    GUEST = "guest"

class RoomType(Enum):
    """Defines available room types"""
    BEDROOM = "bedroom"
    BATHROOM = "bathroom"
    KITCHEN = "kitchen"
    LIVING_ROOM = "living_room"
    OTHER = "other"

class DeviceType(Enum):
    """Defines supported device types"""
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    SECURITY_CAMERA = "security_camera"
    DOOR_LOCK = "door_lock"
    OTHER = "other"

# Core data structures
@dataclass
class Location:
    """Geographic location data"""
    latitude: float
    longitude: float

class User:
    """User data structure with authentication and contact info"""
    def __init__(self, name: str, username: str, phone_number: str, email: str, privilege: UserPrivilege):
        self.id = str(uuid.uuid4())
        self.name = name
        self.username = username
        self.phone_number = phone_number
        self.email = email
        self.privilege = privilege
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def is_admin(self) -> bool:
        # Check if user has admin privileges
        return self.privilege == UserPrivilege.ADMIN

    def is_kid(self) -> bool:
        # Check if user has kid privileges
        return self.privilege == UserPrivilege.REGULAR

@dataclass
class House:
    """House data structure with location and occupancy info"""
    id: str
    name: str
    address: str
    location: Location
    owner_ids: List[str]
    occupant_count: int
    created_at: datetime
    updated_at: datetime

    def __init__(self, name: str, address: str, location: Location, owner_ids: List[str], occupant_count: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.location = location
        self.owner_ids = owner_ids
        self.occupant_count = occupant_count
        self.created_at = datetime.now()
        self.updated_at = self.created_at

@dataclass
class Room:
    id: str
    name: str
    floor: int
    size: float  # in square meters/feet
    house_id: str
    type: RoomType
    created_at: datetime
    updated_at: datetime

    def __init__(self, name: str, floor: int, size: float, house_id: str, type: RoomType):
        self.id = str(uuid.uuid4())
        self.name = name
        self.floor = floor
        self.size = size
        self.house_id = house_id
        self.type = type
        self.created_at = datetime.now()
        self.updated_at = self.created_at

@dataclass
class Device:
    id: str
    type: DeviceType
    name: str
    room_id: str
    settings: Dict
    status: bool
    last_data: Dict
    last_updated: datetime
    created_at: datetime
    updated_at: datetime

    def __init__(self, type: DeviceType, name: str, room_id: str):
        self.id = str(uuid.uuid4())
        self.type = type
        self.name = name
        self.room_id = room_id
        self.settings = {}
        self.status = False
        self.last_data = {}
        self.last_updated = datetime.now()
        self.created_at = datetime.now()
        self.updated_at = self.created_at

# API implementations
class UserAPI:
    """Handles user management operations"""
    @staticmethod
    def create_user(name: str, username: str, phone: str, email: str, privilege: UserPrivilege) -> User:
        if not name or not username or not phone or not email:
            raise UserError("All user fields (name, username, phone, email) are required")
        if not isinstance(privilege, UserPrivilege):
            raise UserError(f"Invalid privilege type: {privilege}")
        
        return User(name, username, phone, email, privilege)

    @staticmethod
    def get_user(user_id: str) -> Optional[User]:
        if not user_id:
            raise UserError("User ID cannot be empty")
        return None

    @staticmethod
    def update_user(user: User) -> bool:
        if not isinstance(user, User):
            raise UserError("Invalid user object")
        return True

    @staticmethod
    def delete_user(user_id: str) -> bool:
        if not user_id:
            raise UserError("User ID cannot be empty")
        return True

class HouseAPI:
    """Handles house management operations"""
    @staticmethod
    def create_house(name: str, address: str, location: Location, owner_ids: List[str], occupant_count: int) -> House:
        if not name or not address:
            raise HouseError("House name and address are required")
        if not isinstance(location, Location):
            raise HouseError("Invalid location object")
        if not owner_ids:
            raise HouseError("At least one owner ID is required")
        if occupant_count < 1:
            raise HouseError("Occupant count must be positive")
        
        return House(name, address, location, owner_ids, occupant_count)

    @staticmethod
    def get_house(house_id: str) -> Optional[House]:
        if not house_id:
            raise HouseError("House ID cannot be empty")
        return None

    @staticmethod
    def update_house(house: House) -> bool:
        # TODO: Implement database update
        pass

    @staticmethod
    def delete_house(house_id: str) -> bool:
        # TODO: Implement database deletion
        pass

class RoomAPI:
    @staticmethod
    def create_room(name: str, floor: int, size: float, house_id: str, type: RoomType) -> Room:
        if not name or not house_id:
            raise RoomError("Room name and house ID are required")
        if floor < 0:
            raise RoomError("Floor number cannot be negative")
        if size <= 0:
            raise RoomError("Room size must be positive")
        if not isinstance(type, RoomType):
            raise RoomError(f"Invalid room type: {type}")
        
        return Room(name, floor, size, house_id, type)

    @staticmethod
    def get_room(room_id: str) -> Optional[Room]:
        # TODO: Implement database lookup
        pass

    @staticmethod
    def get_rooms_by_house(house_id: str) -> List[Room]:
        if not house_id:
            raise RoomError("House ID cannot be empty")
        return []

    @staticmethod
    def update_room(room: Room) -> bool:
        # TODO: Implement database update
        pass

    @staticmethod
    def delete_room(room_id: str) -> bool:
        # TODO: Implement database deletion
        pass

class DeviceAPI:
    """Handles device management operations"""
    @staticmethod
    def create_device(type: DeviceType, name: str, room_id: str) -> Device:
        if not name or not room_id:
            raise DeviceError("Device name and room ID are required")
        if not isinstance(type, DeviceType):
            raise DeviceError(f"Invalid device type: {type}")
        
        return Device(type, name, room_id)

    @staticmethod
    def get_device(device_id: str) -> Optional[Device]:
        # TODO: Implement database lookup
        pass

    @staticmethod
    def get_devices_by_room(room_id: str) -> List[Device]:
        # TODO: Implement database lookup
        pass

    @staticmethod
    def update_device(device: Device) -> bool:
        # TODO: Implement database update
        pass

    @staticmethod
    def delete_device(device_id: str) -> bool:
        # TODO: Implement database deletion
        pass

    @staticmethod
    def update_device_settings(device_id: str, settings: Dict) -> bool:
        if not device_id:
            raise DeviceError("Device ID cannot be empty")
        if not isinstance(settings, dict):
            raise DeviceError("Settings must be a dictionary")
        return True

    @staticmethod
    def update_device_status(device_id: str, status: bool) -> bool:
        if not device_id:
            raise DeviceError("Device ID cannot be empty")
        if not isinstance(status, bool):
            raise DeviceError("Status must be a boolean value")
        return True
