# ZigStar CC2538 Flasher - Complete Documentation

## Overview

The ZigStar CC2538 Flasher is a Home Assistant add-on that allows you to flash Z-Stack firmware to ZigStar CC2538-based coordinators over the network. The add-on is configured via the Home Assistant frontend; no separate web interface is exposed.

## Architecture

- **Service script**: Reads add-on configuration and orchestrates download/extract and flashing
- **Flasher** (`zigstar-flasher`): Python script handling preparation, readiness wait, and calling cc2538-bsl
- **Container**: Alpine-based image with Python, curl, unzip, and cc2538-bsl

## Prerequisites

- ZigStar device with CC2538 chip, reachable over HTTP and telnet from Home Assistant
- Compatible Z-Stack firmware file (.bin) or a URL (direct .bin or .zip)

## Installation

1. Add repository: `https://github.com/bytelink-ai/zigstar`
2. Install the "ZigStar CC2538 FW Flasher" add-on
3. Configure options in the add-on UI

## Configuration

```yaml
device_ip: "192.168.1.50"
device_port: "23"
firmware_url: ""              # Optional: .bin or .zip URL
firmware_zip_inner: ""        # Optional: inner .bin path when URL is a zip
firmware_file: ""             # Optional: local file under /share
baud_rate: "115200"
prepare_device: true
wait_time: 30
erase_flash: true
verify_flash: true
```

- If `firmware_url` is set and points to a `.zip`, the add-on extracts it and uses the first `.bin` found unless `firmware_zip_inner` is set.
- If `firmware_url` is empty, the add-on uses `firmware_file` from `/share`.

## Usage

1. Provide the firmware via URL or copy a file to `/share`
2. Configure device IP/port and firmware options
3. Start the add-on and monitor logs in the Supervisor UI

## Flashing Flow

1. Prepare device via HTTP: `POST http://<device_ip>/switch/zigbee_update/turn_on`
2. Wait until telnet on `<device_ip>:<port>` is reachable (up to `wait_time`)
3. Test connection
4. Flash via `cc2538-bsl` over telnet with optional erase/verify

## Examples

### URL (ZIP) with inner path
```yaml
firmware_url: "https://example.com/CC2652RB_coordinator_20250321.zip"
firmware_zip_inner: "CC2652RB_coordinator_20250321.bin"
```

### Local file from /share
```yaml
firmware_file: "CC2652RB_coordinator_20250321.bin"
```

## Troubleshooting

- Increase `wait_time` for slower devices (up to 120s)
- Ensure the device is reachable from Home Assistant
- If ZIP contains multiple candidates, set `firmware_zip_inner`
- Check logs for detailed error messages (download/extract/connection)

## Development

Build with GitHub Actions or locally using Docker. The workflow builds per-architecture using appropriate Home Assistant base images.

```bash
# Clone repository
git clone https://github.com/bytelink-ai/zigstar.git
cd zigstar/zigstar-cc2538-flasher

# Local build (single arch example)
docker build \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.15 \
  --build-arg TEMPIO_VERSION=2023.12.0 \
  --build-arg BUILD_ARCH=amd64 \
  -t zigstar-cc2538-flasher:local .
```

## Credits

- [JelmerT/cc2538-bsl](https://github.com/JelmerT/cc2538-bsl)
- [Koenkk/Z-Stack-firmware](https://github.com/Koenkk/Z-Stack-firmware)
- [mercenaruss/zigstar_addons](https://github.com/mercenaruss/zigstar_addons)
