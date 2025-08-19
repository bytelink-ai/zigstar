# Changelog

## [1.0.0] - 2025-01-XX

### Added
- Initial release of ZigStar CC2538 FW Flasher
- **Automatic Device Preparation**: Automatically puts device into ZigBee update mode via HTTP
- **Smart Device Detection**: Waits for device to be ready before flashing
- **4-Step Flashing Process**: Prepare → Wait → Test → Flash workflow
- Network-based firmware flashing via telnet
- Support for Z-Stack 3.x.0 firmware
- Configurable device IP, port, and baud rate
- Optional flash erase and verification
- Integration with cc2538-bsl tool
- Multi-architecture support (aarch64, amd64, armhf, armv7, i386)
- Web interface with device preparation controls
- Configurable wait times for device readiness

### Features
- **Device Preparation**: HTTP endpoint integration for ZigBee update mode
- **Connection Monitoring**: Automatic detection of device readiness
- **Progressive Flashing**: Step-by-step process with detailed logging
- **Flexible Configuration**: Skip preparation or customize wait times
- **Comprehensive Error Handling**: Better error messages and recovery
- **Web UI Enhancements**: Separate prepare and flash buttons
- **Automatic Module Installation**: Requests library for HTTP communication
- **Service Integration**: Seamless Home Assistant add-on experience
- **Support for Various CC2538-based ZigStar Devices**: Wide device compatibility
