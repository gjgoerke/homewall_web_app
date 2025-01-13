# Home Climbing Wall with LEDs
A IoT-based LED control system for climbing walls, built with ESP32 and Django. 
This app is very much a work in progress! I'm currently rewriting it in react-native + expo for mobile. 


## Technical Overview

### Hardware
- ESP32 microcontroller with WiFi connectivity
- WS2811 LED strips (350 addressable LEDs)

### Software Stack
- **Embedded**: 
  - ESP32 firmware with real-time LED control
  - WebServer implementation for REST API
  - JSON-based communication protocol
  - Static IP configuration for reliable connectivity

- **Backend**: 
  - Django web framework
  - SQLite database for boulder storage
  - REST API for LED control

- **Frontend**:
  - Interactive SVG-based wall visualization
  - Real-time LED control interface
  - Responsive design with Bootstrap

## Key Features
- Real-time LED control over WiFi
- JSON-based communication protocol
- SVG-based interactive wall interface
- Support for different hold types (start, finish, feet-only, etc.)
- Configurable network settings

## Technical Implementation Details

### Embedded System
The ESP32 firmware (see `led/led/src/main.cpp`) implements:
- HTTP server for receiving commands
- Real-time LED control
- JSON parsing for command processing
- Static IP configuration for reliable networking

### Network Communication
- REST API for LED control
- JSON payload structure for hold data
- Error handling and status reporting
- CORS support for web security

