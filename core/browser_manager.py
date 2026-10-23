#!/usr/bin/env python3
"""
Chrome Browser Manager for AutoApply
Launches Chrome in remote debugging mode (CDP) and manages tabs.
"""

import os
import sys
import time
import urllib.request
import subprocess
from pathlib import Path

DEFAULT_PORT = 9222

def find_chrome_executable() -> str:
    """Finds Chrome executable across standard Windows, macOS, and Linux locations."""
    if sys.platform.startswith("win"):
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for p in candidates:
            if os.path.isfile(p):
                return p
    elif sys.platform == "darwin":
        mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.isfile(mac_path):
            return mac_path
    else:
        # Linux
        for bin_name in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium"]:
            res = subprocess.run(["which", bin_name], capture_output=True, text=True)
            if res.returncode == 0:
                return res.stdout.strip()
    return "chrome"

def is_cdp_available(port: int = DEFAULT_PORT) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1.5) as res:
            return res.status == 200
    except Exception:
        return False

def ensure_chrome_running(port: int = DEFAULT_PORT, user_data_dir: Path = None):
    """Ensures Google Chrome is running with CDP enabled on the target port."""
    if is_cdp_available(port):
        return True

    chrome_bin = find_chrome_executable()
    if not user_data_dir:
        user_data_dir = Path.home() / ".autoapply_chrome_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Launching Chrome with remote debugging on port {port}...")
    cmd = [
        chrome_bin,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={str(user_data_dir)}",
        "--no-first-run",
        "--no-default-browser-check",
        "--start-maximized"
    ]
    subprocess.Popen(cmd)
    
    # Wait for CDP to come up
    for _ in range(15):
        time.sleep(0.5)
        if is_cdp_available(port):
            print("✅ Chrome CDP connected successfully!\n")
            return True

    print("⚠️ Warning: Chrome started but CDP port not yet responding. Retrying...")
    return is_cdp_available(port)
