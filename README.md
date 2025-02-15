# Smart Home System API Assignment

A Python implementation of Smart Home System APIs for managing users, houses, rooms, and devices. This project was developed as part of BU EC530 Spring 2024.

## Assignment Requirements

- Design APIs for core entities (User, House, Room, Device)
- Develop stub builds for the APIs
- Create unit tests for stub functions
- Implement GitHub Actions for automation
- Design appropriate data structures and error handling

## Project Structure

- `shs_api.py`: Core API implementations with data structures and stub functions
- `tests/tests_shs_api.py`: Comprehensive unit tests for all API functions
- `.github/workflows/python-app.yml`: GitHub Actions configuration for CI
- `requirements.txt`: Project dependencies

## API Components

### Data Structures
- User: Manages user information with privilege levels (Admin, Regular, Kid)
- House: Handles house details including location and ownership
- Room: Manages different room types within houses
- Device: Controls various smart devices and their states

### API Classes
- UserAPI: User management operations
- HouseAPI: House management functions
- RoomAPI: Room organization methods
- DeviceAPI: Device control and monitoring

## Testing

Run the test suite:
