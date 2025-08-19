# ZigStar CC2538 FW Flasher

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

Flash Z-Stack firmware to ByteLink Exodus1 over the network.

## About

This add-on allows you to flash Z-Stack firmware to your ZigStar CC2538 devices directly from Home Assistant. It uses the [cc2538-bsl](https://github.com/JelmerT/cc2538-bsl) tool to communicate with the device over telnet and flash the firmware.

## Features

- **Automatic Device Preparation**: Automatically puts device into ZigBee update mode
- **Network-based Firmware Flashing**: No physical connection required
- **Support for Z-Stack 3.x.0 Firmware**: Compatible with latest Z-Stack releases
- **Configurable Baud Rate and Connection Parameters**: Flexible communication settings
- **Optional Flash Erase and Verification**: Customize the flashing process
- **Smart Device Detection**: Waits for device to be ready before flashing
- **Easy Integration with Home Assistant**: Seamless add-on experience

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "ZigStar CC2538 FW Flasher" add-on
3. Configure the device settings
4. Upload your Z-Stack firmware file to the `/share` directory
5. Start the add-on to begin flashing

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `device_ip` | `192.168.1.100` | IP address of your ZigStar device |
| `device_port` | `23` | Telnet port (usually 23) |
| `firmware_file` | `""` | Name of the firmware file in `/share` directory |
| `baud_rate` | `115200` | Baud rate for communication |
| `prepare_device` | `true` | Automatically put device in ZigBee update mode |
| `wait_time` | `30` | Maximum wait time for device readiness (10-120 seconds) |
| `erase_flash` | `true` | Erase flash before writing new firmware |
| `verify_flash` | `true` | Verify flash after writing |

## Usage

### Prerequisites

1. **Device Setup**: Ensure your ZigStar device is accessible via HTTP and telnet
2. **Network Access**: The device must be reachable from your Home Assistant instance
3. **Firmware File**: Download the appropriate Z-Stack firmware (e.g., [CC2652RB_coordinator_20250321.zip](https://github.com/Koenkk/Z-Stack-firmware/blob/Z-Stack_3.x.0_router_20250403/coordinator/Z-Stack_3.x.0/bin/CC2652RB_coordinator_20250321.zip))

### Flashing Process

The add-on follows a 4-step process:

1. **Prepare Device**: Sends HTTP request to put device in ZigBee update mode
2. **Wait for Ready**: Monitors device until it's available for flashing
3. **Test Connection**: Verifies telnet connectivity
4. **Flash Firmware**: Uploads new firmware using cc2538-bsl tool

### Steps

1. **Upload Firmware**: Place your firmware file in the `/share` directory
2. **Configure Settings**: Set device IP, port, and firmware filename
3. **Start Flashing**: Start the add-on to begin the automated process
4. **Monitor Progress**: Check the logs for detailed progress information

### Example Configuration

```yaml
device_ip: "192.168.1.50"
device_port: "23"
firmware_file: "CC2652RB_coordinator_20250321.bin"
baud_rate: "115200"
prepare_device: true
wait_time: 45
erase_flash: true
verify_flash: true
```

## Supported Firmware

This add-on is designed to work with Z-Stack firmware files, particularly:
- Z-Stack 3.x.0 coordinator firmware
- CC2652RB coordinator firmware
- Other compatible CC2538 firmware files

## Troubleshooting

### Connection Issues
- Verify the device IP address is correct
- Ensure the device is accessible via HTTP (for preparation)
- Check that the telnet port is accessible
- Verify network connectivity

### Device Preparation Issues
```
Error: Could not put device in update mode
```
**Solutions:**
- Check if device supports the `/switch/zigbee_update/turn_on` endpoint
- Verify HTTP connectivity to the device
- Check device logs for any error messages

### Flashing Issues
- Verify the firmware file is compatible with your device
- Ensure the device has sufficient power during flashing
- Check the logs for specific error messages
- Verify device is in proper bootloader mode

### Common Errors
- **"Connection failed"**: Check network connectivity and device IP
- **"Firmware file not found"**: Verify the file is uploaded to `/share` directory
- **"Device not ready after waiting"**: Increase wait_time or check device status
- **"Flashing failed"**: Check device compatibility and firmware format

## Advanced Usage

### Manual Device Preparation
If you prefer to manually prepare the device, you can:

1. Set `prepare_device: false` in the configuration
2. Manually send: `curl -X POST http://device-ip/switch/zigbee_update/turn_on`
3. Wait for the device to enter update mode
4. Start the add-on

### Custom Wait Times
Adjust the `wait_time` based on your device:
- **Fast devices**: 15-30 seconds
- **Slower devices**: 45-60 seconds
- **Very slow devices**: 90-120 seconds

### Command Line Usage
For advanced users, you can execute commands directly:

```bash
# Test connection only
zigstar-flasher --device-ip 192.168.1.50 --device-port 23 --firmware /share/firmware.bin --test-only

# Flash with custom options
zigstar-flasher --device-ip 192.168.1.50 --device-port 23 --firmware /share/firmware.bin --baud-rate 115200 --erase --verify --wait-time 45

# Skip device preparation
zigstar-flasher --device-ip 192.168.1.50 --device-port 23 --firmware /share/firmware.bin --skip-prepare
```

## Credits

- [JelmerT/cc2538-bsl](https://github.com/JelmerT/cc2538-bsl) - CC2538 bootloader tool
- [Koenkk/Z-Stack-firmware](https://github.com/Koenkk/Z-Stack-firmware) - Z-Stack firmware
- [mercenaruss/zigstar_addons](https://github.com/mercenaruss/zigstar_addons) - Inspiration and reference

## License

This project is licensed under the Apache License 2.0.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
