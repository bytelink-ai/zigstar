#!/usr/bin/env python3
"""
Simple web interface for ZigStar CC2538 Flasher
"""

import os
import json
import subprocess
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class ZigStarHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = self.get_html()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/flash':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            
            # Extract parameters
            device_ip = data.get('device_ip', [''])[0]
            device_port = data.get('device_port', ['23'])[0]
            firmware_file = data.get('firmware_file', [''])[0]
            baud_rate = data.get('baud_rate', ['115200'])[0]
            erase_flash = data.get('erase_flash', ['false'])[0] == 'true'
            verify_flash = data.get('verify_flash', ['false'])[0] == 'true'
            prepare_device = data.get('prepare_device', ['true'])[0] == 'true'
            wait_time = int(data.get('wait_time', ['30'])[0])
            
            # Execute flashing
            result = self.execute_flash(
                device_ip, device_port, firmware_file, 
                baud_rate, erase_flash, verify_flash,
                prepare_device, wait_time
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'success': result}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/prepare':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode())
            
            device_ip = data.get('device_ip', [''])[0]
            
            # Execute device preparation
            result = self.prepare_device(device_ip)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'success': result}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def prepare_device(self, device_ip):
        """Put device into ZigBee update mode"""
        try:
            url = f"http://{device_ip}/switch/zigbee_update/turn_on"
            print(f"Putting device into ZigBee update mode: {url}")
            
            response = requests.post(url, timeout=10)
            
            if response.status_code == 200:
                print("✓ Device successfully put into ZigBee update mode")
                return True
            else:
                print(f"✗ Failed to put device in update mode. Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error putting device in update mode: {e}")
            return False
    
    def execute_flash(self, device_ip, device_port, firmware_file, baud_rate, erase_flash, verify_flash, prepare_device, wait_time):
        """Execute the firmware flashing"""
        try:
            firmware_path = f"/share/{firmware_file}"
            if not os.path.exists(firmware_path):
                return False
            
            cmd = [
                "zigstar-flasher",
                "--device-ip", device_ip,
                "--device-port", device_port,
                "--firmware", firmware_path,
                "--baud-rate", baud_rate,
                "--wait-time", str(wait_time)
            ]
            
            if erase_flash:
                cmd.append("--erase")
            
            if verify_flash:
                cmd.append("--verify")
            
            if not prepare_device:
                cmd.append("--skip-prepare")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error executing flash: {e}")
            return False
    
    def get_html(self):
        """Generate the HTML interface"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>ZigStar CC2538 Flasher</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 700px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input[type="text"], input[type="number"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        .checkbox-group { display: flex; align-items: center; }
        input[type="checkbox"] { margin-right: 10px; }
        button { background-color: #007cba; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; margin-bottom: 10px; }
        button:hover { background-color: #005a87; }
        button:disabled { background-color: #ccc; cursor: not-allowed; }
        .btn-secondary { background-color: #6c757d; }
        .btn-secondary:hover { background-color: #545b62; }
        .status { margin-top: 20px; padding: 15px; border-radius: 5px; display: none; }
        .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .info { background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .step-indicator { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .step-indicator h3 { margin-top: 0; color: #495057; }
        .step-indicator ol { margin: 0; padding-left: 20px; }
        .step-indicator li { margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ZigStar CC2538 Flasher</h1>
        
        <div class="step-indicator">
            <h3>Flashing Process:</h3>
            <ol>
                <li><strong>Prepare Device:</strong> Put device into ZigBee update mode</li>
                <li><strong>Wait for Ready:</strong> Device becomes available for flashing</li>
                <li><strong>Test Connection:</strong> Verify telnet connectivity</li>
                <li><strong>Flash Firmware:</strong> Upload new firmware</li>
            </ol>
        </div>
        
        <form id="flashForm">
            <div class="form-group">
                <label for="device_ip">Device IP Address:</label>
                <input type="text" id="device_ip" name="device_ip" value="192.168.1.100" required>
            </div>
            
            <div class="form-group">
                <label for="device_port">Device Port:</label>
                <input type="number" id="device_port" name="device_port" value="23" min="1" max="65535" required>
            </div>
            
            <div class="form-group">
                <label for="firmware_file">Firmware File (in /share directory):</label>
                <input type="text" id="firmware_file" name="firmware_file" placeholder="e.g., CC2652RB_coordinator_20250321.bin" required>
            </div>
            
            <div class="form-group">
                <label for="baud_rate">Baud Rate:</label>
                <input type="number" id="baud_rate" name="baud_rate" value="115200" required>
            </div>
            
            <div class="form-group">
                <label for="wait_time">Wait Time (seconds):</label>
                <input type="number" id="wait_time" name="wait_time" value="30" min="10" max="120" required>
            </div>
            
            <div class="form-group">
                <div class="checkbox-group">
                    <input type="checkbox" id="prepare_device" name="prepare_device" checked>
                    <label for="prepare_device">Prepare device (put in ZigBee update mode)</label>
                </div>
            </div>
            
            <div class="form-group">
                <div class="checkbox-group">
                    <input type="checkbox" id="erase_flash" name="erase_flash" checked>
                    <label for="erase_flash">Erase flash before writing</label>
                </div>
            </div>
            
            <div class="form-group">
                <div class="checkbox-group">
                    <input type="checkbox" id="verify_flash" name="verify_flash" checked>
                    <label for="verify_flash">Verify flash after writing</label>
                </div>
            </div>
            
            <button type="button" id="prepareButton" class="btn-secondary">Prepare Device Only</button>
            <button type="submit" id="flashButton">Start Complete Flashing Process</button>
        </form>
        
        <div id="status" class="status"></div>
    </div>
    
    <script>
        document.getElementById('prepareButton').addEventListener('click', async function() {
            const button = this;
            const status = document.getElementById('status');
            const deviceIp = document.getElementById('device_ip').value;
            
            if (!deviceIp) {
                status.className = 'status error';
                status.textContent = 'Please enter a device IP address first.';
                status.style.display = 'block';
                return;
            }
            
            button.disabled = true;
            button.textContent = 'Preparing Device...';
            
            try {
                const response = await fetch('/prepare', {
                    method: 'POST',
                    body: new URLSearchParams({device_ip: deviceIp})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    status.className = 'status success';
                    status.textContent = 'Device successfully put into ZigBee update mode!';
                } else {
                    status.className = 'status error';
                    status.textContent = 'Failed to put device in update mode. Check the logs for details.';
                }
            } catch (error) {
                status.className = 'status error';
                status.textContent = 'Error: ' + error.message;
            } finally {
                button.disabled = false;
                button.textContent = 'Prepare Device Only';
                status.style.display = 'block';
            }
        });
        
        document.getElementById('flashForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const button = document.getElementById('flashButton');
            const status = document.getElementById('status');
            
            button.disabled = true;
            button.textContent = 'Flashing...';
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/flash', {
                    method: 'POST',
                    body: new URLSearchParams(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    status.className = 'status success';
                    status.textContent = 'Firmware flashing completed successfully!';
                } else {
                    status.className = 'status error';
                    status.textContent = 'Firmware flashing failed. Check the logs for details.';
                }
            } catch (error) {
                status.className = 'status error';
                status.textContent = 'Error: ' + error.message;
            } finally {
                button.disabled = false;
                button.textContent = 'Start Complete Flashing Process';
                status.style.display = 'block';
            }
        });
    </script>
</body>
</html>
        """

def main():
    """Start the web server"""
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('', port), ZigStarHandler)
    print(f"Starting ZigStar Flasher web interface on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    main()
