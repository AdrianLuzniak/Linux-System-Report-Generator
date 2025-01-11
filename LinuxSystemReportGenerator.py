import os
import psutil
import platform
import getpass
import subprocess
import socket
import pandas as pd
from datetime import datetime


def collect_system_info():
    system_info = {
        "System": platform.system(),
        "Hostname": socket.gethostname(),
        "Architecture": platform.architecture()[0],
        "Kernel Version": platform.release(),
        "OS Version": platform.version(),
        "Machine type": platform.machine(),
        "Processor": platform.processor(),
        "CPU Count": psutil.cpu_count(logical=True),
        "Memory Total (GB)": round(psutil.virtual_memory().total / (1024**3), 2),  # Convert bytes to gigabytes
        "Memory Available (GB)": round(psutil.virtual_memory().available / (1024**3), 2),
        "Disk Total (GB)": round(psutil.disk_usage("/").total / (1024**3), 2),
        "Disk Used (GB)": round(psutil.disk_usage("/").used / (1024**3), 2),
        "Disk Free (GB)": round(psutil.disk_usage("/").free / (1024**3), 2),
        "Swap Total (GB)": round(psutil.swap_memory().total / (1024**3), 2),
        "Swap Used (GB)": round(psutil.swap_memory().used / (1024**3), 2),
        "Swap Free (GB)": round(psutil.swap_memory().free / (1024**3), 2),
        "Uptime (days)": get_uptime_in_days(),
        "Python Version": platform.python_version(),
        "Current User": getpass.getuser(),
        "Superuser(s)": get_superusers(),
    }
    print(system_info)


def get_uptime_in_days():
    current_time = datetime.now()

    system_start_time = datetime.fromtimestamp(
        psutil.boot_time()
    )  # psutil.boot_time() returns the time in seconds that the system was started (in UNIX timestamp format)
    uptime_seconds = (current_time - system_start_time).total_seconds()
    uptime_days = round(uptime_seconds / (24 * 3600), 2)
    return uptime_days


def get_superusers():
    superusers = []
    with open("/etc/sudoers", "r") as f:
        for line in f:
            if "ALL=(ALL:ALL)" in line:
                superusers.append(line.split()[0])
    return ", ".join(superusers)


def main():
    system_info = collect_system_info()
    print(f"System information saved to file")


if __name__ == "__main__":
    main()
