from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from shs_api.shs_api import UserAPI, UserPrivilege, HouseAPI, RoomAPI, DeviceAPI, Location, Room as ShsRoom, RoomType, DeviceType
from shs_api import models
from shs_api import schemas
from shs_api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Smart Home System API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------
# User Endpoints
# --------------------------
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Convert the string to the actual UserPrivilege enum
        privilege_enum = UserPrivilege(user.privilege)
        new_user = UserAPI.create_user(
            user.name,
            user.username,
            user.phone_number,
            user.email,
            privilege_enum
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    db_user = models.User(
        name=new_user.name,
        username=new_user.username,
        phone_number=new_user.phone_number,
        email=new_user.email,
        privilege=new_user.privilege.value  # Convert enum to string
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: str, updated_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        privilege_enum = UserPrivilege(updated_data.privilege)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update fields
    db_user.name = updated_data.name
    db_user.username = updated_data.username
    db_user.phone_number = updated_data.phone_number
    db_user.email = updated_data.email
    db_user.privilege = privilege_enum.value  # Store the enum's value (e.g., "admin")

    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}

# --------------------------
# House Endpoints
# --------------------------
@app.post("/houses/", response_model=schemas.HouseResponse)
def create_house(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    try:
        loc = Location(latitude=house.latitude, longitude=house.longitude)
        new_house = HouseAPI.create_house(house.name, house.address, loc, house.owner_ids, house.occupant_count)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    db_house = models.House(
        name=new_house.name,
        address=new_house.address,
        latitude=new_house.location.latitude,
        longitude=new_house.location.longitude,
        owner_ids=new_house.owner_ids,
        occupant_count=new_house.occupant_count
    )
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

@app.get("/houses/{house_id}", response_model=schemas.HouseResponse)
def get_house(house_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a house by its ID.
    """
    db_house = db.query(models.House).filter(models.House.id == house_id).first()
    if not db_house:
        raise HTTPException(status_code=404, detail="House not found")
    return db_house


@app.put("/houses/{house_id}", response_model=schemas.HouseResponse)
def update_house(house_id: str, house_update: schemas.HouseCreate, db: Session = Depends(get_db)):
    """
    Update an existing house.
    
    Note: For simplicity, we're using the same schema for update as for create.
    In a production app, you might want a separate schema with optional fields.
    """
    db_house = db.query(models.House).filter(models.House.id == house_id).first()
    if not db_house:
        raise HTTPException(status_code=404, detail="House not found")
    
    db_house.name = house_update.name
    db_house.address = house_update.address
    db_house.latitude = house_update.latitude
    db_house.longitude = house_update.longitude
    db_house.owner_ids = house_update.owner_ids
    db_house.occupant_count = house_update.occupant_count

    db.commit()
    db.refresh(db_house)
    return db_house


@app.delete("/houses/{house_id}", response_model=dict)
def delete_house(house_id: str, db: Session = Depends(get_db)):
    """
    Delete a house by its ID.
    """
    db_house = db.query(models.House).filter(models.House.id == house_id).first()
    if not db_house:
        raise HTTPException(status_code=404, detail="House not found")
    db.delete(db_house)
    db.commit()
    return {"detail": "House deleted"}

# --------------------------
# Room Endpoints
# --------------------------
@app.post("/rooms/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    try:
        # Convert the room type from string to enum for business logic
        room_type = RoomType(room.type)
        new_room = RoomAPI.create_room(room.name, room.floor, room.size, room.house_id, room_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    db_room = models.Room(
        name=new_room.name,
        floor=new_room.floor,
        size=new_room.size,
        house_id=new_room.house_id,
        type=new_room.type.value  # Convert enum to string for storage
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@app.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
def get_room(room_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a room by its ID.
    """
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


@app.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: str, room_update: schemas.RoomCreate, db: Session = Depends(get_db)):
    """
    Update an existing room.
    
    For simplicity, we're using the same schema for updates as for creation.
    """
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Update room details
    db_room.name = room_update.name
    db_room.floor = room_update.floor
    db_room.size = room_update.size
    db_room.house_id = room_update.house_id
    db_room.type = room_update.type  

    db.commit()
    db.refresh(db_room)
    return db_room


@app.delete("/rooms/{room_id}", response_model=dict)
def delete_room(room_id: str, db: Session = Depends(get_db)):
    """
    Delete a room by its ID.
    """
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"detail": "Room deleted"}

# --------------------------
# Device Endpoints
# --------------------------
@app.post("/devices/", response_model=schemas.DeviceResponse)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    try:
        device_type = DeviceType(device.type)
        new_device = DeviceAPI.create_device(device_type, device.name, device.room_id)
        new_device.settings = device.settings or {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_device = models.Device(
        type=new_device.type.value,  
        name=new_device.name,
        room_id=new_device.room_id,
        settings=new_device.settings,
        status=new_device.status,
        last_data=new_device.last_data,
        last_updated=new_device.last_updated
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.get("/devices/{device_id}", response_model=schemas.DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a device by its ID.
    """
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@app.put("/devices/{device_id}", response_model=schemas.DeviceResponse)
def update_device(device_id: str, device_update: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Check if device_update.type is already a DeviceType
    if isinstance(device_update.type, DeviceType):
        device_type_enum = device_update.type
    else:
        try:
            device_type_enum = DeviceType(device_update.type)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid device type")
    
    
    db_device.type = device_type_enum.value
    db_device.name = device_update.name
    db_device.room_id = device_update.room_id
    db_device.settings = device_update.settings  
    
    db.commit()
    db.refresh(db_device)
    return db_device


@app.delete("/devices/{device_id}", response_model=dict)
def delete_device(device_id: str, db: Session = Depends(get_db)):
    """
    Delete a device by its ID.
    """
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(db_device)
    db.commit()
    return {"detail": "Device deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)