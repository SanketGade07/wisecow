
import psutil
import logging
import os
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
CPU_THRESHOLD = 80      # in %
MEMORY_THRESHOLD = 80   # in %
DISK_THRESHOLD = 80     # in %
LOG_PATH = os.path.expanduser("~/system_health.log")

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message, level="info"):
    """Print and log messages simultaneously."""
    print(message)
    if level == "warning":
        logging.warning(message)
    else:
        logging.info(message)

def check_system_health():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    alert_triggered = False
    status_message = f"\nSystem Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(status_message)
    logging.info(status_message)

    # Check metrics and log alerts
    if cpu > CPU_THRESHOLD:
        log_and_print(f"⚠️ ALERT: CPU usage high at {cpu:.1f}%", "warning")
        alert_triggered = True
    if memory > MEMORY_THRESHOLD:
        log_and_print(f"⚠️ ALERT: Memory usage high at {memory:.1f}%", "warning")
        alert_triggered = True
    if disk > DISK_THRESHOLD:
        log_and_print(f"⚠️ ALERT: Disk usage high at {disk:.1f}%", "warning")
        alert_triggered = True

    # Always show summary of current usage
    log_and_print(f"📊 Current usage — CPU:{cpu:.1f}% | MEM:{memory:.1f}% | DISK:{disk:.1f}%")

    # If no issues, print OK summary
    if not alert_triggered:
        log_and_print("✅ System operating within normal limits")

    # Top processes by CPU
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                       key=lambda p: p.info['cpu_percent'],
                       reverse=True)[:5]
    print("\nTop 5 processes by CPU usage:")
    for p in processes:
        print(f"PID {p.info['pid']:>5} | CPU {p.info['cpu_percent']:>5.1f}% | {p.info['name']}")
    print("-" * 60)

if __name__ == "__main__":
    check_system_health()
    print(f"Logs written to: {LOG_PATH}")
