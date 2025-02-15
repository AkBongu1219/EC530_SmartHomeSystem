from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import uuid

# Base exception hierarchy for the system
class SmartHomeError(Exception):
    """Base exception class for Smart Home System"""
    pass

class UserError(SmartHomeError):
    """Exceptions for user-related operations"""
    pass

class HouseError(SmartHomeError):
    """Exceptions for house-related operations"""
    pass

class RoomError(SmartHomeError):
    """Exceptions for room-related operations"""
    pass

class DeviceError(SmartHomeError):
    """Exceptions for device-related operations"""
    pass

# System enums for type safety
class UserPrivilege(Enum):
    """Defines user access levels in the system"""
    ADMIN = "admin"
    REGULAR = "regular"
    KID = "kid"

class RoomType(Enum):
    """Defines available room types"""
    BEDROOM = "bedroom"
    BATHROOM = "bathroom" 
    KITCHEN = "kitchen"
    HALLWAY = "hallway"
    OTHER = "other"

class DeviceType(Enum):
    """Defines supported device types"""
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    LOCK = "lock"
    SENSOR = "sensor"
    OTHER = "other"

# Core data structures
@dataclass
class Location:
    """Geographic location data"""
    latitude: float
    longitude: float

@dataclass 
class User:
    """User data structure with authentication and contact info"""
    id: str
    name: str
    username: str
    phone_number: str
    email: str
    privilege: UserPrivilege
    
    def __init__(self, name: str, username: str, phone_number: str, email: str, privilege: UserPrivilege):
        # Generate unique ID for new user
        self.id = str(uuid.uuid4())
        self.name = name
        self.username = username
        self.phone_number = phone_number
        self.email = email
        self.privilege = privilege

    def is_admin(self) -> bool:
        # Check if user has admin privileges
        return self.privilege == UserPrivilege.ADMIN

    def is_kid(self) -> bool:
        # Check if user has kid privileges
        return self.privilege == UserPrivilege.KID

@dataclass
class House:
    """House data structure with location and occupancy info"""
    id: str
    name: str
    address: str
    location: Location
    owner_ids: List[str]
    occupant_count: int

    def __init__(self, name: str, address: str, location: Location, owner_ids: List[str], occupant_count: int):
        # Generate unique ID for new house
        self.id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.location = location
        self.owner_ids = owner_ids
        self.occupant_count = occupant_count

@dataclass
class Room:
    id: str
    name: str
    floor: int
    size: float  # in square meters/feet
    house_id: str
    type: RoomType

    def __init__(self, name: str, floor: int, size: float, house_id: str, type: RoomType):
        self.id = str(uuid.uuid4())
        self.name = name
        self.floor = floor
        self.size = size
        self.house_id = house_id
        self.type = type

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

    def __init__(self, type: DeviceType, name: str, room_id: str):
        self.id = str(uuid.uuid4())
        self.type = type
        self.name = name
        self.room_id = room_id
        self.settings = {}
        self.status = False
        self.last_data = {}
        self.last_updated = datetime.now()

# API implementations
class UserAPI:
    """Handles user management operations"""
    @staticmethod
    def create_user(name: str, username: str, phone: str, email: str, privilege: UserPrivilege) -> User:
        # Validate required fields
        if not name or not username or not phone or not email:
            raise UserError("All user fields (name, username, phone, email) are required")
        if not isinstance(privilege, UserPrivilege):
            raise UserError(f"Invalid privilege type: {privilege}")
        return User(name, username, phone, email, privilege)

    @staticmethod
    def get_user(user_id: str) -> Optional[User]:
        # Validate user ID
        if not user_id:
            raise UserError("User ID cannot be empty")
        # TODO: Implement database lookup
        pass

    @staticmethod
    def update_user(user: User) -> bool:
        if not isinstance(user, User):
            raise UserError("Invalid user object")
        # TODO: Implement database update
        pass

    @staticmethod
    def delete_user(user_id: str) -> bool:
        # TODO: Implement database deletion
        pass

class HouseAPI:
    """Handles house management operations"""
    @staticmethod
    def create_house(name: str, address: str, location: Location, owner_ids: List[str], occupant_count: int) -> House:
        # Validate house creation parameters
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
        # TODO: Implement database lookup
        pass

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
        # TODO: Implement database lookup
        pass

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
        # Validate device creation parameters
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
        # Validate settings update parameters
        if not device_id:
            raise DeviceError("Device ID cannot be empty")
        if not isinstance(settings, dict):
            raise DeviceError("Settings must be a dictionary")
        # TODO: Implement settings update
        pass

    @staticmethod
    def update_device_status(device_id: str, status: bool) -> bool:
        # Validate status update parameters
        if not device_id:
            raise DeviceError("Device ID cannot be empty")
        if not isinstance(status, bool):
            raise DeviceError("Status must be a boolean value")
        # TODO: Implement status update
        pass
