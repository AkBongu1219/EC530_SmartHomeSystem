# EC530 Smart Home System API

Assignment implementation for BU EC530 Smart Home System API project.

## Assignment Requirements Met

### API Design
- Implemented core entities: User, House, Room, Device
- Created data structures using Python dataclasses
- Developed error handling with custom exceptions

### API Components
- UserAPI: User management with privilege levels
- HouseAPI: House management with location tracking
- RoomAPI: Room organization with type classification
- DeviceAPI: Device control with status monitoring

### Implementation
- Stub builds for all API functions
- Comprehensive unit tests for each API
- Error handling and input validation
- GitHub Actions for automated testing

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests/
```

## Project Structure
- `shs_api.py`: Core API implementations
- `tests/tests_shs_api.py`: Unit tests
- `.github/workflows/python-app.yml`: CI configuration

## GitHub Repository
[EC530_SmartHomeSystem](https://github.com/AkBongu1219/EC530_SmartHomeSystem)

## Author
Akhil Bongu
```
