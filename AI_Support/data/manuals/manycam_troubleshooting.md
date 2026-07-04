# ManyCam Camera Troubleshooting Guide

This troubleshooting guide provides instructions for fixing common camera issues in ManyCam.

## 1. Camera Not Detected

If ManyCam shows "No Camera Found" or the camera is not in the list of available sources:
- **Operating System Permissions:**
  - **Windows:** Go to *Settings > Privacy > Camera* and ensure "Allow apps to access your camera" is turned ON.
  - **macOS:** Go to *System Preferences > Security & Privacy > Privacy > Camera* and check ManyCam.
- **USB Port Speed and Power:** Connect the camera directly to a USB 3.0 port (blue port). Avoid using front ports on desktop cases or unpowered hubs.
- **Device Manager Verification (Windows):** Open Device Manager and expand *Cameras* or *Imaging Devices*. Verify if the camera is listed without warning signs.
- **Driver Reinstallation:** Right-click the camera in Device Manager, choose *Uninstall Device*, unplug the camera, restart the PC, and plug it back in.

## 2. Fixing the Black Screen Issue

A black screen is usually caused by source conflicts or graphic card configurations.
- **Source Conflicts:** Ensure other software (like Zoom, Teams, Skype, or OBS) is not actively using the camera. Close all other apps and restart ManyCam.
- **Hardware Acceleration:** In ManyCam, go to *Settings > General* and toggle Hardware Acceleration off or on, then restart ManyCam.
- **ManyCam Driver Reset:**
  - Open ManyCam, click the camera slot, select a different source, then switch back.
  - Reinstall ManyCam Virtual Webcam driver from the Settings menu.

## 3. Audio Issues (No Sound or Echo)

- **Input Selection:** Verify that the correct microphone device is selected in ManyCam's audio settings.
- **Echo Cancellation:** Check the "Echo Cancellation" box in ManyCam audio options if your speakers are bleeding sound into the microphone.
- **Sample Rate Mismatch:** Set both ManyCam audio and your Windows recording device sample rate to 48000 Hz or 44100 Hz in Windows Sound Control Panel.
