import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from shs_api import (
    UserAPI, HouseAPI, RoomAPI, DeviceAPI,
    User, House, Room, Device,
    UserPrivilege, RoomType, DeviceType, Location
)

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.test_user_data = {
            "name": "John Doe",
            "username": "johndoe",
            "phone_number": "1234567890",
            "email": "john@example.com",
            "privilege": UserPrivilege.REGULAR
        }
        
    def test_create_user(self):
        create_user_params = {
            "name": self.test_user_data["name"],
            "username": self.test_user_data["username"],
            "phone": self.test_user_data["phone_number"],
            "email": self.test_user_data["email"],
            "privilege": self.test_user_data["privilege"]
        }
        user = UserAPI.create_user(**create_user_params)
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, self.test_user_data["name"])
        self.assertEqual(user.privilege, self.test_user_data["privilege"])
        
    @patch('shs_api.UserAPI.get_user')
    def test_get_user(self, mock_get):
        user_init_data = {
            "name": self.test_user_data["name"],
            "username": self.test_user_data["username"],
            "phone_number": self.test_user_data["phone_number"],
            "email": self.test_user_data["email"],
            "privilege": self.test_user_data["privilege"]
        }
        mock_user = User(**user_init_data)
        mock_get.return_value = mock_user
        
        result = UserAPI.get_user("test-id")
        self.assertEqual(result, mock_user)
        
        mock_get.return_value = None
        result = UserAPI.get_user("non-existent-id")
        self.assertIsNone(result)
        
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

class TestHouseAPI(unittest.TestCase):
    def setUp(self):
        self.test_location = Location(latitude=40.7128, longitude=-74.0060)
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
        self.assertEqual(house.occupant_count, self.test_house_data["occupant_count"])
        
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

class TestRoomAPI(unittest.TestCase):
    def setUp(self):
        self.test_room_data = {
            "name": "Master Bedroom",
            "floor": 2,
            "size": 30.5,
            "house_id": "test-house-id",
            "type": RoomType.BEDROOM
        }
        
    def test_create_room(self):
        room = RoomAPI.create_room(**self.test_room_data)
        self.assertIsInstance(room, Room)
        self.assertEqual(room.name, self.test_room_data["name"])
        self.assertEqual(room.type, self.test_room_data["type"])
        
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

class TestDeviceAPI(unittest.TestCase):
    def setUp(self):
        self.test_device_data = {
            "type": DeviceType.LIGHT,
            "name": "Living Room Light",
            "room_id": "test-room-id"
        }
        
    def test_create_device(self):
        device = DeviceAPI.create_device(**self.test_device_data)
        self.assertIsInstance(device, Device)
        self.assertEqual(device.name, self.test_device_data["name"])
        self.assertEqual(device.type, self.test_device_data["type"])
        self.assertFalse(device.status)
        self.assertIsInstance(device.last_updated, datetime)
        
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

if __name__ == '__main__':
    unittest.main()