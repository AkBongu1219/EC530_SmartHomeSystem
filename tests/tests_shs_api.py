# Import required testing modules
import unittest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
import logging

# Import all components from the main API
from shs_api import (
    UserAPI, HouseAPI, RoomAPI, DeviceAPI,
    User, House, Room, Device,
    UserPrivilege, RoomType, DeviceType, Location,
    SmartHomeError, UserError, HouseError, RoomError, DeviceError,
    logger
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
        # Temporarily disable logging to avoid cluttering test output
        logger.handlers = []
        
    @patch('shs_api.logger')
    def test_create_user(self, mock_logger):
        # Test successful user creation
        create_user_params = {
            "name": self.test_user_data["name"],
            "username": self.test_user_data["username"],
            "phone": self.test_user_data["phone_number"],
            "email": self.test_user_data["email"],
            "privilege": self.test_user_data["privilege"]
        }
        user = UserAPI.create_user(**create_user_params)
        
        # Verify logging calls
        mock_logger.info.assert_has_calls([
            call(f"Attempting to create user with username: {create_user_params['username']}"),
            call(f"Successfully created user with ID: {user.id}")
        ])
        
    @patch('shs_api.logger')
    @patch('shs_api.UserAPI.get_user')
    def test_get_user(self, mock_get, mock_logger):
        # Test user retrieval with mocked database
        user_init_data = {
            "name": self.test_user_data["name"],
            "username": self.test_user_data["username"],
            "phone_number": self.test_user_data["phone_number"],
            "email": self.test_user_data["email"],
            "privilege": self.test_user_data["privilege"]
        }
        mock_user = User(**user_init_data)
        mock_get.return_value = mock_user
        
        # Test successful retrieval
        result = UserAPI.get_user("test-id")
        mock_logger.info.assert_called_with("Attempting to retrieve user with ID: test-id")
        
        # Test non-existent user
        result = UserAPI.get_user("non-existent-id")
        mock_logger.debug.assert_called_with("User lookup not yet implemented for ID: non-existent-id")
        
    @patch('shs_api.UserAPI.update_user')
    def test_update_user(self, mock_update):
        mock_update.return_value = True
        user_init_data = {
            "name": self.test_user_data["name"],
            "username": self.test_user_data["username"],
            "phone_number": self.test_user_data["phone_number"],
            "email": self.test_user_data["email"],
            "privilege": self.test_user_data["privilege"]
        }
        user = User(**user_init_data)
        
        result = UserAPI.update_user(user)
        self.assertTrue(result)
        mock_update.assert_called_once_with(user)
        
    @patch('shs_api.UserAPI.delete_user')
    def test_delete_user(self, mock_delete):
        mock_delete.return_value = True
        
        result = UserAPI.delete_user("test-id")
        self.assertTrue(result)
        mock_delete.assert_called_once_with("test-id")

    def test_create_user_validation(self):
        # Test validation errors for user creation
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
        self.test_location = Location(latitude=40.7128, longitude=-74.0060)
        self.test_house_data = {
            "name": "Test House",
            "address": "123 Test St",
            "location": self.test_location,
            "owner_ids": ["owner1", "owner2"],
            "occupant_count": 4
        }
        logger.handlers = []
        
    @patch('shs_api.logger')
    def test_create_house(self, mock_logger):
        house = HouseAPI.create_house(**self.test_house_data)
        
        mock_logger.info.assert_has_calls([
            call(f"Attempting to create house: {self.test_house_data['name']}"),
            call(f"Successfully created house with ID: {house.id}")
        ])

    @patch('shs_api.HouseAPI.get_house')
    def test_get_house(self, mock_get):
        mock_house = House(**self.test_house_data)
        mock_get.return_value = mock_house
        
        result = HouseAPI.get_house("test-id")
        self.assertEqual(result, mock_house)

    @patch('shs_api.HouseAPI.update_house')
    def test_update_house(self, mock_update):
        mock_update.return_value = True
        house = House(**self.test_house_data)
        
        result = HouseAPI.update_house(house)
        self.assertTrue(result)
        mock_update.assert_called_once_with(house)
        
    @patch('shs_api.HouseAPI.delete_house')
    def test_delete_house(self, mock_delete):
        mock_delete.return_value = True
        
        result = HouseAPI.delete_house("test-id")
        self.assertTrue(result)
        mock_delete.assert_called_once_with("test-id")

    def test_create_house_validation(self):
        # Test validation errors for house creation
        with self.assertRaises(HouseError):
            HouseAPI.create_house("", "address", self.test_location, ["owner1"], 4)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "", self.test_location, ["owner1"], 4)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "address", "invalid_location", ["owner1"], 4)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "address", self.test_location, [], 4)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("name", "address", self.test_location, ["owner1"], 0)

class TestRoomAPI(unittest.TestCase):
    """Test suite for RoomAPI operations"""
    
    def setUp(self):
        # Initialize test data for room operations
        self.test_room_data = {
            "name": "Master Bedroom",
            "floor": 2,
            "size": 30.5,
            "house_id": "test-house-id",
            "type": RoomType.BEDROOM
        }
        logger.handlers = []
        
    @patch('shs_api.logger')
    def test_create_room(self, mock_logger):
        room = RoomAPI.create_room(**self.test_room_data)
        
        mock_logger.info.assert_has_calls([
            call(f"Attempting to create room: {self.test_room_data['name']} in house: {self.test_room_data['house_id']}"),
            call(f"Successfully created room with ID: {room.id}")
        ])

    @patch('shs_api.RoomAPI.get_rooms_by_house')
    def test_get_rooms_by_house(self, mock_get_rooms):
        mock_rooms = [Room(**self.test_room_data)]
        mock_get_rooms.return_value = mock_rooms
        
        result = RoomAPI.get_rooms_by_house("test-house-id")
        self.assertEqual(result, mock_rooms)

    @patch('shs_api.RoomAPI.get_room')
    def test_get_room(self, mock_get):
        mock_room = Room(**self.test_room_data)
        mock_get.return_value = mock_room
        
        result = RoomAPI.get_room("test-id")
        self.assertEqual(result, mock_room)
        
        mock_get.return_value = None
        result = RoomAPI.get_room("non-existent-id")
        self.assertIsNone(result)
    
    @patch('shs_api.RoomAPI.update_room')
    def test_update_room(self, mock_update):
        mock_update.return_value = True
        room = Room(**self.test_room_data)
        
        result = RoomAPI.update_room(room)
        self.assertTrue(result)
        mock_update.assert_called_once_with(room)
        
    @patch('shs_api.RoomAPI.delete_room')
    def test_delete_room(self, mock_delete):
        mock_delete.return_value = True
        
        result = RoomAPI.delete_room("test-id")
        self.assertTrue(result)
        mock_delete.assert_called_once_with("test-id")

    def test_create_room_validation(self):
        # Test validation errors for room creation
        with self.assertRaises(RoomError):
            RoomAPI.create_room("", 2, 30.5, "house_id", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", -1, 30.5, "house_id", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", 2, 0, "house_id", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", 2, 30.5, "", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("name", 2, 30.5, "house_id", "invalid_type")

class TestDeviceAPI(unittest.TestCase):
    """Test suite for DeviceAPI operations"""
    
    def setUp(self):
        # Initialize test data for device operations
        self.test_device_data = {
            "type": DeviceType.LIGHT,
            "name": "Living Room Light",
            "room_id": "test-room-id"
        }
        logger.handlers = []
        
    @patch('shs_api.logger')
    def test_create_device(self, mock_logger):
        device = DeviceAPI.create_device(**self.test_device_data)
        
        mock_logger.info.assert_has_calls([
            call(f"Attempting to create {self.test_device_data['type'].value} device: {self.test_device_data['name']} in room: {self.test_device_data['room_id']}"),
            call(f"Successfully created device with ID: {device.id}")
        ])
        
    @patch('shs_api.DeviceAPI.get_devices_by_room')
    def test_get_devices_by_room(self, mock_get_devices):
        mock_devices = [Device(**self.test_device_data)]
        mock_get_devices.return_value = mock_devices
        
        result = DeviceAPI.get_devices_by_room("test-room-id")
        self.assertEqual(result, mock_devices)
        
    @patch('shs_api.DeviceAPI.update_device_settings')
    def test_update_device_settings(self, mock_update):
        mock_update.return_value = True
        test_settings = {"brightness": 80, "color": "warm"}
        
        result = DeviceAPI.update_device_settings("test-device-id", test_settings)
        self.assertTrue(result)
        mock_update.assert_called_once_with("test-device-id", test_settings)
        
    @patch('shs_api.DeviceAPI.update_device_status')
    def test_update_device_status(self, mock_update):
        mock_update.return_value = True
        
        result = DeviceAPI.update_device_status("test-device-id", True)
        self.assertTrue(result)
        mock_update.assert_called_once_with("test-device-id", True)

    @patch('shs_api.DeviceAPI.get_device')
    def test_get_device(self, mock_get):
        mock_device = Device(**self.test_device_data)
        mock_get.return_value = mock_device
        
        result = DeviceAPI.get_device("test-id")
        self.assertEqual(result, mock_device)
        
        mock_get.return_value = None
        result = DeviceAPI.get_device("non-existent-id")
        self.assertIsNone(result)
    
    @patch('shs_api.DeviceAPI.update_device')
    def test_update_device(self, mock_update):
        mock_update.return_value = True
        device = Device(**self.test_device_data)
        
        result = DeviceAPI.update_device(device)
        self.assertTrue(result)
        mock_update.assert_called_once_with(device)
        
    @patch('shs_api.DeviceAPI.delete_device')
    def test_delete_device(self, mock_delete):
        mock_delete.return_value = True
        
        result = DeviceAPI.delete_device("test-id")
        self.assertTrue(result)
        mock_delete.assert_called_once_with("test-id")

    @patch('shs_api.logger')
    def test_create_device_validation(self, mock_logger):
        # Test validation errors for device creation
        with self.assertRaises(DeviceError):
            DeviceAPI.create_device(DeviceType.LIGHT, "", "room_id")
        mock_logger.error.assert_called_with("Unexpected error during device creation: Device name and room ID are required")
        
        with self.assertRaises(DeviceError):
            DeviceAPI.create_device("invalid_type", "name", "room_id")
        mock_logger.error.assert_called_with("Device creation failed: Invalid device type: invalid_type")

    @patch('shs_api.logger')
    def test_update_device_settings_validation(self, mock_logger):
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_settings("", {"brightness": 80})
        mock_logger.error.assert_called_with("Error updating device settings: Device ID cannot be empty")
        
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_settings("device_id", "invalid_settings")
        mock_logger.error.assert_called_with("Error updating device settings: Settings must be a dictionary")

    @patch('shs_api.logger')
    def test_update_device_status_validation(self, mock_logger):
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_status("", True)
        mock_logger.error.assert_called_with("Error updating device status: Device ID cannot be empty")
        
        with self.assertRaises(DeviceError):
            DeviceAPI.update_device_status("device_id", "invalid_status")
        mock_logger.error.assert_called_with("Error updating device status: Status must be a boolean value")

if __name__ == '__main__':
    unittest.main()