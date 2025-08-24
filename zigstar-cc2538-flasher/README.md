# ZigStar CC2538 FW Flasher

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

Flash Z-Stack firmware to ZigStar CC2538 based coordinators over the network using the cc2538-bsl tool.

## About

This add-on allows you to flash Z-Stack 3.x.0 coordinator firmware to your ZigStar CC2538 devices directly from Home Assistant. It uses the [cc2538-bsl](https://github.com/JelmerT/cc2538-bsl) tool to communicate with the device over telnet and flash the firmware.

**Recommended Firmware**: [Z-Stack 3.x.0 Coordinator Firmware](https://github.com/Koenkk/Z-Stack-firmware/tree/Z-Stack_3.x.0_router_20250403/coordinator/Z-Stack_3.x.0)

## Features

- **Automatic Device Preparation**: Automatically puts device into ZigBee update mode
- **Network-based Firmware Flashing**: No physical connection required
- **Firmware URL Support**: Download firmware from a URL (ZIP or BIN)
- **ZIP Inner Path**: Select inner .bin from a ZIP automatically or explicitly
- **Configurable Baud Rate**: Flexible communication settings
- **Optional Flash Erase and Verification**
- **Smart Device Detection**: Waits for device to be ready before flashing

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "ZigStar CC2538 FW Flasher" add-on
3. Configure the device settings in the add-on UI
4. Start the add-on to begin flashing

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `device_ip` | `192.168.1.100` | IP address of your ZigStar device |
| `device_port` | `23` | Telnet port (usually 23) |
| `firmware_url` | `""` | Optional: URL to firmware (.bin or .zip) |
| `firmware_zip_inner` | `""` | Optional: inner .bin path inside ZIP |
| `firmware_file` | `""` | Optional: name of local file in `/share` |
| `baud_rate` | `115200` | Baud rate for communication |
| `prepare_device` | `true` | Automatically put device in ZigBee update mode |
| `wait_time` | `30` | Maximum wait time for device readiness (10-120 seconds) |
| `erase_flash` | `true` | Erase flash before writing new firmware |
| `verify_flash` | `true` | Verify flash after writing |

Notes:
- If `firmware_url` is set, the add-on downloads it into the container. If the URL points to a `.zip`, it will extract it and pick the first `.bin`, unless `firmware_zip_inner` is provided to select a specific path.
- If `firmware_url` is empty, the add-on uses `firmware_file` from the `/share` folder.

## Example Configurations

### Download and flash Z-Stack 3.x.0 coordinator firmware
device_ip: "192.168.1.50"
device_port: "23"
firmware_url: "https://github.com/Koenkk/Z-Stack-firmware/raw/Z-Stack_3.x.0_router_20250403/coordinator/Z-Stack_3.x.0/bin/CC2652RB_coordinator_20250321.zip"
firmware_zip_inner: "CC2652RB_coordinator_20250321.hex.bin"
baud_rate: "115200"
prepare_device: true
wait_time: 45
erase_flash: true
verify_flash: true
```

### Use local file from /share
```yaml
device_ip: "192.168.1.50"
device_port: "23"
firmware_file: "CC2652RB_coordinator_20250321.bin"
baud_rate: "115200"
prepare_device: true
wait_time: 30
erase_flash: true
verify_flash: true
```

## Flashing Process

The add-on follows a 4-step process:

1. **Prepare Device**: Sends HTTP request to put device in ZigBee update mode (`/switch/zigbee_update/turn_on`)
2. **Wait for Ready**: Monitors device until it's available for flashing (telnet open)
3. **Test Connection**: Verifies telnet connectivity
4. **Flash Firmware**: Uploads new firmware using cc2538-bsl tool

## Troubleshooting

- Verify device is reachable via HTTP and telnet from Home Assistant
- If ZIP has multiple binaries, specify `firmware_zip_inner`
- Increase `wait_time` for slower devices (up to 120s)
- Ensure power is stable during flashing

## Credits

- [JelmerT/cc2538-bsl](https://github.com/JelmerT/cc2538-bsl) - CC2538 bootloader tool and patch
- [Koenkk/Z-Stack-firmware](https://github.com/Koenkk/Z-Stack-firmware) - Z-Stack firmware
- [mercenaruss/zigstar_addons](https://github.com/mercenaruss/zigstar_addons) - Add-on architecture inspiration

## License

This project is licensed under the Apache License 2.0.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
