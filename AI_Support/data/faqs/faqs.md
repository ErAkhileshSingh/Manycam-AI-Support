# Frequently Asked Questions (FAQs)
Here are the most common questions and quick answers for PTZ cameras and ManyCam setup.
## Q1: Why is my camera not detected?
**Answer:** This usually occurs due to driver conflicts, privacy permissions, or USB power limits. Ensure the camera is plugged into a USB 3.0 port directly on the PC. On Windows, check *Privacy Settings > Camera* to make sure ManyCam has permission to access the camera. Check if the camera is visible in Device Manager.
## Q2: Why is my PTZ preset not working?
**Answer:** PTZ presets fail if there is an IP mismatch or if the ONVIF port configuration is wrong. Verify the camera IP is reachable, and make sure that you are using the correct ONVIF/VISCA command port (default is 80, 8080, or 5678). Also check if the preset was saved properly on the camera's internal storage.
## Q3: What should I do if the RTSP connection failed?
**Answer:** Double-check the RTSP URL format. It should include the username, password, camera IP, port (554), and stream path. For example: `rtsp://admin:password@192.168.1.100:554/h264Preview_01_main`. Verify that the camera is reachable via ping from the PC.
## Q4: Why is there no audio coming from my stream?
**Answer:** Check that the correct audio device is selected under ManyCam Audio Settings. Ensure the microphone is not muted in Windows Control Panel. Ensure that ManyCam has Microphone permissions enabled in your OS privacy settings.
## Q5: How do I resolve a ManyCam Streaming Issue?
**Answer:** If you experience lag or RTMP streaming failures:
- Check your internet upload speed (needs to be at least 5 Mbps for stable 1080p).
- Lower the resolution in ManyCam to 720p at 30 FPS.
- Verify that your stream key and RTMP Server URL are correct.
- Ensure Windows Defender Firewall is not blocking ManyCam outbound traffic.
## Q6: Why do I get a camera connection problem?
**Answer:** For USB cameras, check cable lengths (should be under 5 meters for USB 2.0 and 3 meters for USB 3.0 unless active/optical cables are used). For network cameras, ensure the camera and computer are on the same local subnet.
## Q7: How do I fix a License activation issue?
**Answer:** Ensure you are logged into your ManyCam account inside the software. If you exceed the device activation limit, log into your ManyCam dashboard online and deactivate the software on older devices.
