# Import required testing modules
import unittest
from datetime import datetime

# Import all components from the main API
from shs_api import (
    UserAPI, HouseAPI, RoomAPI, DeviceAPI,
    User, House, Room, Device,
    UserPrivilege, RoomType, DeviceType, Location,
    SmartHomeError, UserError, HouseError, RoomError, DeviceError
)

class TestUserAPI(unittest.TestCase):
    """Test suite for UserAPI operations"""
    
    def setUp(self):
        # Initialize test data for user operations
        self.test_user_data = {
            "name": "John Doe",
            "username": "johndoe",
            "phone_number": "1234567890",
            "email": "john@example.com",
            "privilege": UserPrivilege.REGULAR
        }
        
    def test_create_user(self):
        # Test successful user creation
        create_user_params = {
            "name": self.test_user_data["name"],
            "username": self.test_user_data["username"],
            "phone": self.test_user_data["phone_number"],
            "email": self.test_user_data["email"],
            "privilege": self.test_user_data["privilege"]
        }
        user = UserAPI.create_user(**create_user_params)
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, create_user_params["name"])
        
    def test_create_user_validation(self):
        # Test validation errors
        with self.assertRaises(UserError):
            UserAPI.create_user("", "username", "phone", "email", UserPrivilege.REGULAR)
            
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "", "phone", "email", UserPrivilege.REGULAR)
            
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "username", "", "email", UserPrivilege.REGULAR)
            
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "username", "phone", "", UserPrivilege.REGULAR)
            
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "username", "phone", "email", "invalid_privilege")

class TestHouseAPI(unittest.TestCase):
    """Test suite for HouseAPI operations"""
    
    def setUp(self):
        # Initialize test data for house operations
        self.test_location = Location(latitude=42.3601, longitude=-71.0589)
        self.test_house_data = {
            "name": "Test House",
            "address": "123 Test St",
            "location": self.test_location,
            "owner_ids": ["owner1", "owner2"],
            "occupant_count": 4
        }
        
    def test_create_house(self):
        house = HouseAPI.create_house(**self.test_house_data)
        self.assertIsInstance(house, House)
        self.assertEqual(house.name, self.test_house_data["name"])
        
    def test_create_house_validation(self):
        with self.assertRaises(HouseError):
            HouseAPI.create_house("", "address", self.test_location, ["owner1"], 2)
            
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "", self.test_location, ["owner1"], 2)
            
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "address", "invalid_location", ["owner1"], 2)
            
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "address", self.test_location, [], 2)
            
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "address", self.test_location, ["owner1"], 0)

class TestRoomAPI(unittest.TestCase):
    """Test suite for RoomAPI operations"""
    
    def setUp(self):
        # Initialize test data for room operations
        self.test_room_data = {
            "name": "Living Room",
            "floor": 1,
            "size": 20.5,
            "house_id": "test-house-id",
            "type": RoomType.LIVING_ROOM
        }
        
    def test_create_room(self):
        room = RoomAPI.create_room(**self.test_room_data)
        self.assertIsInstance(room, Room)
        self.assertEqual(room.name, self.test_room_data["name"])
        
    def test_create_room_validation(self):
        with self.assertRaises(RoomError):
            RoomAPI.create_room("", 1, 20.5, "house_id", RoomType.BEDROOM)
            
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", -1, 20.5, "house_id", RoomType.BEDROOM)
            
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", 1, 0, "house_id", RoomType.BEDROOM)
            
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", 1, 20.5, "", RoomType.BEDROOM)
            
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", 1, 20.5, "house_id", "invalid_type")

class TestDeviceAPI(unittest.TestCase):
    """Test suite for DeviceAPI operations"""
    
    def setUp(self):
        # Initialize test data for device operations
        self.test_device_data = {
            "type": DeviceType.LIGHT,
            "name": "Living Room Light",
            "room_id": "test-room-id"
        }
        
    def test_create_device(self):
        device = DeviceAPI.create_device(**self.test_device_data)
        self.assertIsInstance(device, Device)
        self.assertEqual(device.name, self.test_device_data["name"])
        
    def test_create_device_validation(self):
        with self.assertRaises(DeviceError):
            DeviceAPI.create_device(DeviceType.LIGHT, "", "room_id")
            
        with self.assertRaises(DeviceError):
            DeviceAPI.create_device("invalid_type", "name", "room_id")
            
    def test_update_device_settings_validation(self):
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_settings("", {"brightness": 80})
            
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_settings("device_id", "invalid_settings")
            
    def test_update_device_status_validation(self):
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_status("", True)
            
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_status("device_id", "invalid_status")

if __name__ == '__main__':
    unittest.main()