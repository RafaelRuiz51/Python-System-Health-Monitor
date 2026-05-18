import psutil          # reads system stats
import datetime        # gets current time
import time            # lets us pause/loop

# --- SETTINGS (you can change these numbers) ---
CPU_THRESHOLD = 80      # warn if CPU goes above 80%
RAM_THRESHOLD = 80      # warn if RAM goes above 80%
DISK_THRESHOLD = 85     # warn if disk goes above 85%
LOG_FILE = "health_log.txt"
CHECK_INTERVAL = 10     # check every 10 seconds

def get_stats():
    """Collect current system stats"""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, ram, disk

def check_alerts(cpu, ram, disk):
    """Check if anything is above our thresholds"""
    alerts = []
    if cpu > CPU_THRESHOLD:
        alerts.append(f"WARNING  HIGH CPU: {cpu}%")
    if ram > RAM_THRESHOLD:
        alerts.append(f"WARNING  HIGH RAM: {ram}%")
    if disk > DISK_THRESHOLD:
        alerts.append(f"WARNING  HIGH DISK: {disk}%")
    return alerts

def log_results(cpu, ram, disk, alerts):
    """Write results to log file and print to screen"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"\n{'='*50}\n"
        f"Timestamp : {timestamp}\n"
        f"CPU Usage : {cpu}%\n"
        f"RAM Usage : {ram}%\n"
        f"Disk Usage: {disk}%\n"
    )

    if alerts:
        log_entry += "ALERTS:\n"
        for alert in alerts:
            log_entry += f"  {alert}\n"
    else:
        log_entry += "Status    : All systems normal\n"

    print(log_entry)

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def run_monitor():
    """Main loop - keeps running until you press Ctrl+C"""
    print("System Health Monitor Started")
    print(f"Logging to: {LOG_FILE}")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            cpu, ram, disk = get_stats()
            alerts = check_alerts(cpu, ram, disk)
            log_results(cpu, ram, disk, alerts)
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitor stopped. Check health_log.txt for full log.")

run_monitor()