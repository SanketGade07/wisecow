#!/usr/bin/env python3
import requests
import time
import logging
import os
import urllib3

# Disable insecure request warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
APP_URL = "https://wisecow.127.0.0.1.nip.io:8443"

CHECK_INTERVAL = 30  # seconds between checks

# Create a safe log directory in your home folder
log_dir = os.path.expanduser("~/app_logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "app_health.log")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_app_health():
    """Check if the application is up and responding correctly."""
    try:
        # Ignore SSL verification for local self-signed certificates
        response = requests.get(APP_URL, timeout=5, verify=False)
        if response.status_code == 200:
            print(f"✅ Application is UP (HTTP {response.status_code})")
            logging.info(f"Application UP - HTTP {response.status_code}")
        else:
            print(f"⚠️ Application reachable but returned status {response.status_code}")
            logging.warning(f"Application issue - HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Application DOWN - {e}")
        logging.error(f"Application DOWN - {e}")

if __name__ == "__main__":
    print(f"Starting application health check for {APP_URL}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            check_app_health()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Health checker stopped by user.")
        logging.info("Health checker stopped by user.")
