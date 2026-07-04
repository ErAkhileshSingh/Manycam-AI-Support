# Connecting and Configuring PTZ Cameras

This guide outlines how to configure motorized PTZ (Pan-Tilt-Zoom) cameras for streaming systems like ManyCam.

## 1. Physical Connections

PTZ Cameras can be connected to your system in three primary ways:
- **USB Interface:** Connect the camera using a USB 3.0 cable directly to a USB port on your PC. Avoid USB hubs to prevent power drops.
- **IP Camera (Network):** Connect the camera to your local network using an Ethernet cable (RJ45). Most PTZ cameras support PoE (Power over Ethernet).
- **NDI (Network Device Interface):** High-quality, low-latency video over IP. Requires NDI-capable software/licenses and a Gigabit network switch.

## 2. Setting Up RTSP Streams

To fetch the video feed from an IP PTZ camera:
1. Identify the camera IP address. Use a IP scanner tool or the camera's utility tool.
2. The default RTSP URL is usually:
   `rtsp://[username]:[password]@[camera_ip]:554/live/ch0` or `/h264Preview_01_main`
3. In ManyCam, click **Add Video Source** -> **IP Camera / RTSP** -> Input the RTSP URL.

## 3. Configuring PTZ Presets

Presets allow you to save camera positions (Pan, Tilt, Zoom) and switch between them instantly.
- **Creating Presets:** Use the camera's IR remote control or the web interface. Move the camera to the desired angle, press `Preset` then a number (e.g., `1`), and press `Enter`.
- **Calling Presets:** Press the preset number on your controller or invoke it via ONVIF/VISCA commands.
- **ManyCam Integration:** You can control PTZ presets via the PTZ control panel in ManyCam if the camera is connected via USB and supports UVC PTZ controls.

## 4. Troubleshooting PTZ Not Moving

If your PTZ camera stops moving or doesn't respond to controls:
- **Check Power supply:** Verify the LED indicator light on the camera. It should be solid blue/green.
- **Protocol Mismatch:** If controlling via VISCA or Pelco-D, verify that the baud rate matches (commonly 9600 bps).
- **IP Network Blocks:** Ensure you can access the camera's web-admin portal. Try pinging the camera IP.
- **ONVIF Port:** ONVIF control usually runs on port 80 or 8080. Check if ONVIF is enabled in the camera settings.
