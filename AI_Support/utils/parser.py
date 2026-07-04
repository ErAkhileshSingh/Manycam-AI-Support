import re

def parse_log_file(file_content_str):
    """
    Parses log file contents. Looks for ERROR, WARNING, and CRITICAL errors,
    summarizes issues, and provides actionable recommendations.
    """
    lines = file_content_str.splitlines()
    errors = []
    warnings = []
    
    # Common error pattern check
    # e.g. 2026-07-04 10:15:30 [ERROR] USB camera connection timed out
    # e.g. 2026-07-04 10:15:32 [WARN] Failed to open audio device
    
    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()
        if "error" in line_lower or "critical" in line_lower or "fatal" in line_lower or "fail" in line_lower:
            errors.append((line_num, line))
        elif "warning" in line_lower or "warn" in line_lower:
            warnings.append((line_num, line))
            
    # Analyze errors to find specific issue signatures
    findings = []
    recommendations = []
    
    combined_log_text = file_content_str.lower()
    
    # 1. Driver Issues
    if "driver" in combined_log_text or "usb" in combined_log_text or "uvc" in combined_log_text:
        findings.append("USB Driver Conflict / Missing Camera Driver")
        recommendations.append("Uninstall any third-party virtual cameras. Open Windows Device Manager, find your camera under 'Cameras', right-click and select 'Uninstall Device', then restart the PC to let Windows reinstall the default UVC driver.")
        
    # 2. Network/RTSP Issues
    if "timeout" in combined_log_text or "rtsp" in combined_log_text or "network" in combined_log_text or "socket" in combined_log_text:
        findings.append("Network Timeout / RTSP Stream Inaccessible")
        recommendations.append("Verify the camera IP is reachable by pinging it. Ensure port 554 (RTSP) and 80/8080 (ONVIF) are not blocked by a firewall, and verify the network stream URL is correct.")
        
    # 3. Audio issues
    if "audio" in combined_log_text or "sound" in combined_log_text or "microphone" in combined_log_text:
        findings.append("Audio Initialization Error")
        recommendations.append("Check ManyCam Audio settings to verify the input microphone is active. Verify sample rates in Windows Recording Devices match ManyCam's rate (48000 Hz).")
        
    # 4. License issues
    if "license" in combined_log_text or "activation" in combined_log_text or "auth" in combined_log_text:
        findings.append("License Authentication Problem")
        recommendations.append("Check if your ManyCam account has run out of device slots. Log in to ManyCam website and deactivate older unused devices.")
        
    # If no matches, but there are error lines, add a generic finding
    if errors and not findings:
        findings.append(f"{len(errors)} general log errors detected")
        recommendations.append("Examine the raw log lines below. Restart ManyCam and clear cache if errors persist.")
        
    # Fallback default if completely clean
    if not errors and not warnings:
        findings.append("No Errors Found")
        recommendations.append("Logs look clean! If you are still experiencing issues, it could be a hardware physical connection issue. Check cables and power inputs.")
        
    return {
        "total_lines": len(lines),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors[:50],       # limit return list size
        "warnings": warnings[:50],
        "findings": findings,
        "recommendations": recommendations
    }
