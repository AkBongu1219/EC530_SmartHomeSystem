import unittest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from main import app, get_db
from shs_api.database import Base
import shs_api.models as models
import shs_api.schemas as schemas
from shs_api.shs_api import (
    UserAPI, HouseAPI, RoomAPI, DeviceAPI,
    User, House, Room, Device,
    UserPrivilege, RoomType, DeviceType, Location,
    UserError, HouseError, RoomError, DeviceError
)

from sqlalchemy.pool import StaticPool

# ------------------------------------------------------------------
#  TEST CONFIG: In-memory SQLite Database + Dependency Override
# ------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # In-memory DB for tests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # Ensures a single connection is reused
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the engine and SessionLocal in shs_api.database so that the entire app uses the test DB.
import shs_api.database as db_mod
db_mod.engine = engine
db_mod.SessionLocal = TestingSessionLocal

def override_get_db():
    """Override the get_db dependency to use an in-memory database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the default get_db dependency in the app.
app.dependency_overrides[get_db] = override_get_db

# Create a test client for calling the API endpoints
client = TestClient(app)


# ------------------------------------------------------------------
#  UNIT TESTS FOR BUSINESS LOGIC (shs_api.py)
# ------------------------------------------------------------------
class TestBusinessLogic(unittest.TestCase):
    """Unit tests for core business logic in shs_api.py (no HTTP layer)."""

    def setUp(self):
        # Sample data for each entity
        self.user_data = {
            "name": "John Doe",
            "username": "johndoe",
            "phone": "1234567890",
            "email": "john@example.com",
            "privilege": UserPrivilege.REGULAR
        }
        self.house_data = {
            "name": "My House",
            "address": "123 Main St",
            "location": Location(latitude=42.3601, longitude=-71.0589),
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 3
        }
        self.room_data = {
            "name": "Living Room",
            "floor": 1,
            "size": 25.0,
            "house_id": str(uuid.uuid4()),
            "type": RoomType.LIVING_ROOM
        }
        self.device_data = {
            "type": DeviceType.LIGHT,
            "name": "Living Room Light",
            "room_id": str(uuid.uuid4())
        }

    # --------------------------
    # UserAPI Tests
    # --------------------------
    def test_create_user_success(self):
        user = UserAPI.create_user(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, self.user_data["name"])
        self.assertEqual(user.privilege, UserPrivilege.REGULAR)

    def test_create_user_missing_fields(self):
        with self.assertRaises(UserError):
            UserAPI.create_user("", "user", "phone", "email", UserPrivilege.REGULAR)
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "", "phone", "email", UserPrivilege.REGULAR)
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "user", "", "email", UserPrivilege.REGULAR)
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "user", "phone", "", UserPrivilege.REGULAR)

    def test_create_user_invalid_privilege(self):
        with self.assertRaises(UserError):
            UserAPI.create_user("name", "user", "phone", "email", "invalid_privilege")

    # --------------------------
    # HouseAPI Tests
    # --------------------------
    def test_create_house_success(self):
        house = HouseAPI.create_house(**self.house_data)
        self.assertIsInstance(house, House)
        self.assertEqual(house.name, self.house_data["name"])

    def test_create_house_validation(self):
        with self.assertRaises(HouseError):
            HouseAPI.create_house("", "Address", self.house_data["location"], ["owner"], 2)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("House", "", self.house_data["location"], ["owner"], 2)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("House", "Address", "invalid_location", ["owner"], 2)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("House", "Address", self.house_data["location"], [], 2)
        with self.assertRaises(HouseError):
            HouseAPI.create_house("House", "Address", self.house_data["location"], ["owner"], 0)

    # --------------------------
    # RoomAPI Tests
    # --------------------------
    def test_create_room_success(self):
        room = RoomAPI.create_room(**self.room_data)
        self.assertIsInstance(room, Room)
        self.assertEqual(room.name, self.room_data["name"])

    def test_create_room_validation(self):
        with self.assertRaises(RoomError):
            RoomAPI.create_room("", 1, 20.0, "house_id", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("Room", -1, 20.0, "house_id", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("Room", 1, 0, "house_id", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("Room", 1, 20.0, "", RoomType.BEDROOM)
        with self.assertRaises(RoomError):
            RoomAPI.create_room("Room", 1, 20.0, "house_id", "invalid_type")

    # --------------------------
    # DeviceAPI Tests
    # --------------------------
    def test_create_device_success(self):
        device = DeviceAPI.create_device(**self.device_data)
        self.assertIsInstance(device, Device)
        self.assertEqual(device.name, self.device_data["name"])

    def test_create_device_validation(self):
        with self.assertRaises(DeviceError):
            DeviceAPI.create_device(DeviceType.LIGHT, "", "room_id")
        with self.assertRaises(DeviceError):
            DeviceAPI.create_device("invalid_type", "DeviceName", "room_id")


# ------------------------------------------------------------------
#  INTEGRATION TESTS FOR API ENDPOINTS (main.py)
# ------------------------------------------------------------------
class TestAPIEndpoints(unittest.TestCase):
    """Integration tests for the REST API using FastAPI TestClient."""

    @classmethod
    def setUpClass(cls):
        """Create all tables in our in-memory test DB before any tests run."""
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        """Drop all tables after all tests to keep things clean."""
        Base.metadata.drop_all(bind=engine)

    # --------------------------
    #  USER ENDPOINTS
    # --------------------------
    def test_create_and_get_user(self):
        payload = {
            "name": "Alice Smith",
            "username": "alicesmith",
            "phone_number": "9876543210",
            "email": "alice@example.com",
            "privilege": "regular"
        }
        # Create user
        resp = client.post("/users/", json=payload)
        self.assertEqual(resp.status_code, 200, resp.text)
        user_id = resp.json()["id"]

        # Get user
        get_resp = client.get(f"/users/{user_id}")
        self.assertEqual(get_resp.status_code, 200, get_resp.text)
        self.assertEqual(get_resp.json()["name"], payload["name"])
        self.assertEqual(get_resp.json()["privilege"], "regular")

    def test_update_user(self):
        # Create user first
        create_payload = {
            "name": "Bob Jones",
            "username": "bobjones",
            "phone_number": "1112223333",
            "email": "bob@example.com",
            "privilege": "regular"
        }
        create_resp = client.post("/users/", json=create_payload)
        self.assertEqual(create_resp.status_code, 200, create_resp.text)
        user_id = create_resp.json()["id"]

        # Update user
        update_payload = {
            "name": "Robert Jones",
            "username": "bobjones",
            "phone_number": "1112223333",
            "email": "robert@example.com",
            "privilege": "admin"
        }
        update_resp = client.put(f"/users/{user_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["name"], "Robert Jones")
        self.assertEqual(updated_data["email"], "robert@example.com")
        self.assertEqual(updated_data["privilege"], "admin")

    def test_delete_user(self):
        # Create user to delete
        payload = {
            "name": "Charlie Brown",
            "username": "charlieb",
            "phone_number": "5554443333",
            "email": "charlie@example.com",
            "privilege": "guest"
        }
        create_resp = client.post("/users/", json=payload)
        self.assertEqual(create_resp.status_code, 200, create_resp.text)
        user_id = create_resp.json()["id"]

        # Delete user
        del_resp = client.delete(f"/users/{user_id}")
        self.assertEqual(del_resp.status_code, 200, del_resp.text)
        self.assertIn("User deleted", del_resp.text)

        # Verify user no longer exists
        get_resp = client.get(f"/users/{user_id}")
        self.assertEqual(get_resp.status_code, 404, get_resp.text)

    # --------------------------
    #  HOUSE ENDPOINTS
    # --------------------------
    def test_create_and_get_house(self):
        payload = {
            "name": "Test House",
            "address": "456 Example Rd",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 3
        }
        # Create house
        resp = client.post("/houses/", json=payload)
        self.assertEqual(resp.status_code, 200, resp.text)
        house_id = resp.json()["id"]

        # Get house
        get_resp = client.get(f"/houses/{house_id}")
        self.assertEqual(get_resp.status_code, 200, get_resp.text)
        self.assertEqual(get_resp.json()["name"], payload["name"])

    def test_update_house(self):
        # Create a house first
        payload = {
            "name": "House for Update",
            "address": "789 Some Rd",
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 2
        }
        create_resp = client.post("/houses/", json=payload)
        self.assertEqual(create_resp.status_code, 200, create_resp.text)
        house_id = create_resp.json()["id"]

        # Update the house
        update_payload = {
            "name": "Updated House",
            "address": "789 Some Rd Updated",
            "latitude": 99.9,
            "longitude": -99.9,
            "owner_ids": payload["owner_ids"],
            "occupant_count": 5
        }
        update_resp = client.put(f"/houses/{house_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["name"], "Updated House")
        self.assertEqual(updated_data["occupant_count"], 5)

    def test_delete_house(self):
        # Create a house to delete
        payload = {
            "name": "Delete House",
            "address": "123 Deletion Rd",
            "latitude": 1.1,
            "longitude": 2.2,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 2
        }
        create_resp = client.post("/houses/", json=payload)
        self.assertEqual(create_resp.status_code, 200, create_resp.text)
        house_id = create_resp.json()["id"]

        # Delete the house
        del_resp = client.delete(f"/houses/{house_id}")
        self.assertEqual(del_resp.status_code, 200, del_resp.text)

        # Verify it no longer exists
        get_resp = client.get(f"/houses/{house_id}")
        self.assertEqual(get_resp.status_code, 404, get_resp.text)

    # --------------------------
    #  ROOM ENDPOINTS
    # --------------------------
    def test_create_and_get_room(self):
        # First, create a house for the room
        house_payload = {
            "name": "Room House",
            "address": "100 Room St",
            "latitude": 35.0,
            "longitude": -120.0,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 2
        }
        house_resp = client.post("/houses/", json=house_payload)
        self.assertEqual(house_resp.status_code, 200, house_resp.text)
        house_id = house_resp.json()["id"]

        # Create room
        room_payload = {
            "name": "Conference Room",
            "floor": 2,
            "size": 35.0,
            "house_id": house_id,
            "type": "living room"  # Must match the enum's string
        }
        resp = client.post("/rooms/", json=room_payload)
        self.assertEqual(resp.status_code, 200, resp.text)
        room_id = resp.json()["id"]

        # Get room
        get_resp = client.get(f"/rooms/{room_id}")
        self.assertEqual(get_resp.status_code, 200, get_resp.text)
        self.assertEqual(get_resp.json()["name"], room_payload["name"])

    def test_update_room(self):
        # Create a house
        house_payload = {
            "name": "Room House 2",
            "address": "200 Room St",
            "latitude": 45.0,
            "longitude": -75.0,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 3
        }
        house_resp = client.post("/houses/", json=house_payload)
        self.assertEqual(house_resp.status_code, 200, house_resp.text)
        house_id = house_resp.json()["id"]

        # Create a room
        room_payload = {
            "name": "Main Room",
            "floor": 1,
            "size": 20.0,
            "house_id": house_id,
            "type": "living room"
        }
        room_resp = client.post("/rooms/", json=room_payload)
        self.assertEqual(room_resp.status_code, 200, room_resp.text)
        room_id = room_resp.json()["id"]

        # Update the room
        update_payload = {
            "name": "Main Hall",
            "floor": 2,
            "size": 50.0,
            "house_id": house_id,
            "type": "other"
        }
        update_resp = client.put(f"/rooms/{room_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["name"], "Main Hall")
        self.assertEqual(updated_data["type"], "other")

    def test_delete_room(self):
        # Create a house
        house_payload = {
            "name": "Room House 3",
            "address": "300 Room St",
            "latitude": 40.0,
            "longitude": -70.0,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 2
        }
        house_resp = client.post("/houses/", json=house_payload)
        self.assertEqual(house_resp.status_code, 200, house_resp.text)
        house_id = house_resp.json()["id"]

        # Create a room
        room_payload = {
            "name": "Extra Room",
            "floor": 3,
            "size": 15.0,
            "house_id": house_id,
            "type": "bedroom"
        }
        room_resp = client.post("/rooms/", json=room_payload)
        self.assertEqual(room_resp.status_code, 200, room_resp.text)
        room_id = room_resp.json()["id"]

        # Delete the room
        del_resp = client.delete(f"/rooms/{room_id}")
        self.assertEqual(del_resp.status_code, 200, del_resp.text)

        # Verify it no longer exists
        get_resp = client.get(f"/rooms/{room_id}")
        self.assertEqual(get_resp.status_code, 404, get_resp.text)

    # --------------------------
    #  DEVICE ENDPOINTS
    # --------------------------
    def test_create_and_get_device(self):
        # Create a house
        house_payload = {
            "name": "Device House",
            "address": "101 Device Ave",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 1
        }
        house_resp = client.post("/houses/", json=house_payload)
        self.assertEqual(house_resp.status_code, 200, house_resp.text)
        house_id = house_resp.json()["id"]

        # Create a room in that house
        room_payload = {
            "name": "Device Room",
            "floor": 1,
            "size": 25.0,
            "house_id": house_id,
            "type": "living room"
        }
        room_resp = client.post("/rooms/", json=room_payload)
        self.assertEqual(room_resp.status_code, 200, room_resp.text)
        room_id = room_resp.json()["id"]

        # Create device
        device_payload = {
            "type": "light",
            "name": "Test Light",
            "room_id": room_id,
            "settings": {"brightness": 75}
        }
        resp = client.post("/devices/", json=device_payload)
        self.assertEqual(resp.status_code, 200, resp.text)
        device_id = resp.json()["id"]

        # Get device
        get_resp = client.get(f"/devices/{device_id}")
        self.assertEqual(get_resp.status_code, 200, get_resp.text)
        self.assertEqual(get_resp.json()["name"], "Test Light")
        self.assertEqual(get_resp.json()["settings"]["brightness"], 75)

    def test_update_device(self):
        # Create house & room first
        house_payload = {
            "name": "Device House 2",
            "address": "202 Device Ave",
            "latitude": 10.0,
            "longitude": 10.0,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 1
        }
        house_resp = client.post("/houses/", json=house_payload)
        self.assertEqual(house_resp.status_code, 200, house_resp.text)
        house_id = house_resp.json()["id"]

        room_payload = {
            "name": "Device Room 2",
            "floor": 2,
            "size": 20.0,
            "house_id": house_id,
            "type": "kitchen"
        }
        room_resp = client.post("/rooms/", json=room_payload)
        self.assertEqual(room_resp.status_code, 200, room_resp.text)
        room_id = room_resp.json()["id"]

        # Create a device
        device_payload = {
            "type": "thermostat",
            "name": "Smart Thermostat",
            "room_id": room_id,
            "settings": {"temperature": 70}
        }
        create_resp = client.post("/devices/", json=device_payload)
        self.assertEqual(create_resp.status_code, 200, create_resp.text)
        device_id = create_resp.json()["id"]

        # Update device
        update_payload = {
            "type": "thermostat",
            "name": "Updated Thermostat",
            "room_id": room_id,
            "settings": {"temperature": 72}
        }
        update_resp = client.put(f"/devices/{device_id}", json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["name"], "Updated Thermostat")
        self.assertEqual(updated_data["settings"]["temperature"], 72)

    def test_delete_device(self):
        # Create house & room
        house_payload = {
            "name": "Device House 3",
            "address": "303 Device Ave",
            "latitude": 5.0,
            "longitude": 5.0,
            "owner_ids": [str(uuid.uuid4())],
            "occupant_count": 1
        }
        house_resp = client.post("/houses/", json=house_payload)
        self.assertEqual(house_resp.status_code, 200, house_resp.text)
        house_id = house_resp.json()["id"]

        room_payload = {
            "name": "Device Room 3",
            "floor": 3,
            "size": 30.0,
            "house_id": house_id,
            "type": "bathroom"
        }
        room_resp = client.post("/rooms/", json=room_payload)
        self.assertEqual(room_resp.status_code, 200, room_resp.text)
        room_id = room_resp.json()["id"]

        # Create a device
        device_payload = {
            "type": "door lock",
            "name": "Front Door Lock",
            "room_id": room_id,
            "settings": {"auto_lock": True}
        }
        create_resp = client.post("/devices/", json=device_payload)
        self.assertEqual(create_resp.status_code, 200, create_resp.text)
        device_id = create_resp.json()["id"]

        # Delete device
        del_resp = client.delete(f"/devices/{device_id}")
        self.assertEqual(del_resp.status_code, 200, del_resp.text)

        # Verify it no longer exists
        get_resp = client.get(f"/devices/{device_id}")
        self.assertEqual(get_resp.status_code, 404, get_resp.text)


# ------------------------------------------------------------------
#  RUN TESTS
# ------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()