from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import uuid

class UserPrivilege(Enum):
    ADMIN = "admin"
    REGULAR = "regular"
    KID = "kid"

class RoomType(Enum):
    BEDROOM = "bedroom"
    BATHROOM = "bathroom" 
    KITCHEN = "kitchen"
    HALLWAY = "hallway"
    OTHER = "other"

class DeviceType(Enum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    LOCK = "lock"
    SENSOR = "sensor"
    OTHER = "other"

@dataclass
class Location:
    latitude: float
    longitude: float

@dataclass 
class User:
    id: str
    name: str
    username: str
    phone_number: str
    email: str
    privilege: UserPrivilege
    
    def __init__(self, name: str, username: str, phone_number: str, email: str, privilege: UserPrivilege):
        self.id = str(uuid.uuid4())
        self.name = name
        self.username = username
        self.phone_number = phone_number
        self.email = email
        self.privilege = privilege

    def is_admin(self) -> bool:
        return self.privilege == UserPrivilege.ADMIN

    def is_kid(self) -> bool:
        return self.privilege == UserPrivilege.KID

@dataclass
class House:
    id: str
    name: str
    address: str
    location: Location
    owner_ids: List[str]
    occupant_count: int

    def __init__(self, name: str, address: str, location: Location, owner_ids: List[str], occupant_count: int):
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

# API Stubs
class UserAPI:
    @staticmethod
    def create_user(name: str, username: str, phone: str, email: str, privilege: UserPrivilege) -> User:
        return User(name, username, phone, email, privilege)

    @staticmethod
    def get_user(user_id: str) -> Optional[User]:
        # TODO: Implement database lookup
        pass

    @staticmethod
    def update_user(user: User) -> bool:
        # TODO: Implement database update
        pass

    @staticmethod
    def delete_user(user_id: str) -> bool:
        # TODO: Implement database deletion
        pass

class HouseAPI:
    @staticmethod
    def create_house(name: str, address: str, location: Location, owner_ids: List[str], occupant_count: int) -> House:
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
    @staticmethod
    def create_device(type: DeviceType, name: str, room_id: str) -> Device:
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
        # TODO: Implement settings update
        pass

    @staticmethod
    def update_device_status(device_id: str, status: bool) -> bool:
        # TODO: Implement status update
        pass
