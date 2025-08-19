# ZigStar CC2538 Flasher - Complete Documentation

## Overview

The ZigStar CC2538 Flasher is a Home Assistant add-on that allows you to flash Z-Stack firmware to ZigStar CC2538-based coordinators over the network. This add-on eliminates the need for physical connections and provides a user-friendly interface for firmware updates.

## Architecture

The add-on consists of several components:

1. **Main Flasher Script** (`zigstar-flasher`): Python script that handles the firmware flashing process
2. **Web Interface** (`web-interface.py`): Simple HTTP server providing a web-based UI
3. **Service Scripts**: Home Assistant service management scripts
4. **Docker Container**: Alpine Linux-based container with Python and cc2538-bsl tool

## Prerequisites

### Device Requirements
- ZigStar device with CC2538 chip
- Device must be in bootloader mode
- Network connectivity (telnet access)
- Compatible Z-Stack firmware file

### Home Assistant Requirements
- Home Assistant Core or Supervised installation
- Access to add-on store
- Network access to ZigStar device

## Installation

### 1. Add Repository
1. Go to **Settings** → **Add-ons** → **Add-on Store**
2. Click the three dots menu (⋮) → **Repositories**
3. Add: `https://github.com/yourusername/zigstar`
4. Click **Add**

### 2. Install Add-on
1. Find "ZigStar CC2538 FW Flasher" in the add-on store
2. Click **Install**
3. Wait for installation to complete

### 3. Configuration
Configure the add-on with your device settings:

```yaml
device_ip: "192.168.1.50"        # Your ZigStar device IP
device_port: "23"                 # Telnet port (usually 23)
firmware_file: "firmware.bin"     # Firmware filename in /share
baud_rate: "115200"               # Communication baud rate
erase_flash: true                 # Erase flash before writing
verify_flash: true                # Verify flash after writing
```

## Usage

### Method 1: Service-based Flashing
1. **Upload Firmware**: Place your `.bin` file in the `/share` directory
2. **Configure Settings**: Set device IP, port, and firmware filename
3. **Start Add-on**: Click **Start** to begin flashing
4. **Monitor Logs**: Check the logs for progress and results

### Method 2: Web Interface
1. **Start Add-on**: Start the add-on normally
2. **Access Web UI**: Open the add-on in a new tab
3. **Configure Settings**: Fill in the form with your device details
4. **Upload Firmware**: Ensure firmware is in `/share` directory
5. **Start Flashing**: Click "Start Flashing" button

### Method 3: Command Line
For advanced users, you can execute commands directly:

```bash
# Test connection
zigstar-flasher --device-ip 192.168.1.50 --device-port 23 --firmware /share/firmware.bin --test-only

# Flash with custom options
zigstar-flasher --device-ip 192.168.1.50 --device-port 23 --firmware /share/firmware.bin --baud-rate 115200 --erase --verify
```

## Firmware Files

### Supported Formats
- `.bin` files (binary firmware)
- Z-Stack 3.x.0 coordinator firmware
- CC2652RB coordinator firmware

### Recommended Firmware
- **Z-Stack 3.x.0**: Latest stable release
- **CC2652RB**: Optimized for CC2652RB chips
- **Custom builds**: Compatible with CC2538 architecture

### Download Sources
- [Z-Stack Firmware Repository](https://github.com/Koenkk/Z-Stack-firmware)
- [Official ZigStar Firmware](https://github.com/mercenaruss/zigstar_addons)

## Troubleshooting

### Common Issues

#### Connection Problems
```
Error: Connection failed. Please check device IP and port.
```
**Solutions:**
- Verify device IP address is correct
- Ensure device is in bootloader mode
- Check network connectivity
- Verify telnet port is accessible

#### Firmware Issues
```
Error: Firmware file not found
```
**Solutions:**
- Upload firmware to `/share` directory
- Check filename spelling
- Ensure file has `.bin` extension
- Verify file permissions

#### Flashing Failures
```
Error: Firmware flashing failed
```
**Solutions:**
- Check device compatibility
- Verify firmware format
- Ensure stable power supply
- Check device bootloader mode

### Debug Mode
Enable debug logging by setting the log level in Home Assistant:

```yaml
logger:
  default: info
  logs:
    custom_components.zigstar_flasher: debug
```

### Log Analysis
Common log patterns and their meanings:

```
[INFO] Starting ZigStar CC2538 Flasher...
[INFO] Device: 192.168.1.50:23
[INFO] Firmware: firmware.bin
[INFO] Connection successful!
[INFO] Starting firmware flash...
[INFO] Firmware flashing completed successfully!
```

## Advanced Configuration

### Custom Baud Rates
Supported baud rates:
- 115200 (default, recommended)
- 57600
- 38400
- 19200
- 9600

### Network Configuration
For complex network setups:

```yaml
# Custom network configuration
device_ip: "10.0.0.100"
device_port: "2323"  # Custom telnet port
timeout: 30           # Connection timeout in seconds
retries: 3            # Number of retry attempts
```

### Security Considerations
- Use dedicated network segment for flashing
- Implement firewall rules if needed
- Consider VPN access for remote flashing
- Monitor access logs

## Development

### Building from Source
```bash
# Clone repository
git clone https://github.com/yourusername/zigstar.git
cd zigstar/zigstar-cc2538-flasher

# Build Docker image
docker build -t zigstar-cc2538-flasher .

# Test locally
docker run -it --rm zigstar-cc2538-flasher
```

### Testing
Run the test suite:
```bash
python3 test_flasher.py
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## API Reference

### Command Line Options
```bash
zigstar-flasher [OPTIONS]

Options:
  --device-ip TEXT      Device IP address [required]
  --device-port TEXT    Device port (default: 23)
  --firmware PATH       Path to firmware file [required]
  --baud-rate TEXT      Baud rate (default: 115200)
  --erase               Erase flash before writing
  --verify              Verify flash after writing
  --help                Show help message
```

### Web API Endpoints
- `GET /` - Web interface
- `POST /flash` - Execute firmware flashing

### Response Format
```json
{
  "success": true,
  "message": "Firmware flashing completed successfully"
}
```

## Support

### Community Resources
- [Home Assistant Community](https://community.home-assistant.io/)
- [ZigStar Discord](https://discord.gg/zigstar)
- [GitHub Issues](https://github.com/yourusername/zigstar/issues)

### Reporting Issues
When reporting issues, include:
- Home Assistant version
- Add-on version
- Device model and firmware
- Error logs
- Steps to reproduce

## License

This project is licensed under the Apache License 2.0. See [LICENSE](../LICENSE) for details.

## Credits

- **cc2538-bsl**: [JelmerT/cc2538-bsl](https://github.com/JelmerT/cc2538-bsl)
- **Z-Stack Firmware**: [Koenkk/Z-Stack-firmware](https://github.com/Koenkk/Z-Stack-firmware)
- **Inspiration**: [mercenaruss/zigstar_addons](https://github.com/mercenaruss/zigstar_addons)
