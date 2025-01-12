import psutil
import platform
import getpass
import subprocess
import socket
import pandas as pd
from datetime import datetime
import shutil
from openpyxl.styles import Border, Side, Alignment


def collect_system_info():
    system_info = {
        "System": platform.system(),
        "Hostname": socket.gethostname(),
        "Architecture": platform.architecture()[0],
        "OS Version": get_os_version(),
        "Kernel Version": platform.release(),
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
    return system_info


def get_os_version():
    try:
        with open("/etc/os-release", "r") as file:
            os_info = file.readlines()
            for line in os_info:
                if line.startswith("PRETTY_NAME"):
                    return line.split("=")[1].strip().strip('"')

    except Exception as e:
        return f"Error: {str(e)}"


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
    try:
        with open("/etc/sudoers", "r") as f:
            for line in f:
                line = line.strip()

                # Skip lines with comment
                if line.startswith("#") or not line:
                    continue

                # Check if line contains user or group, which has sudo rights
                if "ALL=(ALL)" in line:
                    # Check if line contains definition of user or group
                    parts = line.split()
                    if len(parts) > 0:
                        # If this is group which startswith '%' (ex. %wheel)
                        if parts[0].startswith("%"):
                            superusers.append(parts[0][1:])  # Add group name without '%'
                        else:
                            superusers.append(parts[0])  # Add username
    except Exception as e:
        return f"Error: {str(e)}"
    return ", ".join(superusers)


def get_packages():
    "Supports only yum and dnf package managers, can add more to package_managers"

    package_managers = ["dnf", "yum"]
    packages = []

    for manager in package_managers:
        if shutil.which(manager):  # Check if manager if is installed
            try:
                # Check if package manager exists
                if subprocess.run(["which", manager], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                    result = subprocess.run(
                        [manager, "list", "installed"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    if result.returncode == 0 and result.stdout.strip():  # Check it only white spaces exist
                        packages = result.stdout.strip().split("\n")[1:]  # Skip header
                        return [pkg.split()[0] for pkg in packages if pkg]  # Return only package name
            except Exception as e:
                return f"Error using {manager}: {str(e)}"
            return ["No package manager available"]


def save_to_excel(system_info, packages, filename):

    # System data as table klucz-wartość
    system_info_table = list(system_info.items())  # Convert dictionary in list of tuples

    # Create a DataFrame with two columns: 'Key' and 'Value'
    system_info_df = pd.DataFrame(system_info_table, columns=["Key", "Value"])

    # Save installed packages
    packages_df = pd.DataFrame(packages, columns=["Installed packages"])

    # Save both DataFrames to seperate sheets in one Excel file
    with pd.ExcelWriter(filename) as writer:
        system_info_df.to_excel(writer, sheet_name="System Info", index=False)
        packages_df.to_excel(writer, sheet_name="Installed Packages", index=False)

        # Load workbook, to adjust columns
        workbook = writer.book
        system_info_sheet = workbook["System Info"]
        packages_sheet = workbook["Installed Packages"]

        # Ajdust width of column to content size
        for sheet in [system_info_sheet, packages_sheet]:
            for col in sheet.columns:  # sheet.columns - all columns as list, col - list of cells in one column
                max_length = 0
                column = col[0].column_letter  # Get the column letter
                for cell in col:  # Get the longest cell in sheet
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except Exception as e:
                        print(f"Error processing cell {cell.coordinate}: {e}")
                        continue  # Skip to next cell in the column
                adjusted_width = max_length + 2
                sheet.column_dimensions[column].width = adjusted_width

        # Add border to tables in both sheets
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )

        # Center values in columns and add borders
        center_alignment = Alignment(horizontal="center", vertical="center")

        for sheet in [system_info_sheet, packages_sheet]:
            for row in sheet.iter_rows():
                for cell in row:
                    cell.border = thin_border
                    cell.alignment = center_alignment


def main():
    filename = "system_info.xlsx"

    system_info = collect_system_info()

    packages = get_packages()
    save_to_excel(system_info, packages, filename)

    print(f"System information saved to file {filename}")


if __name__ == "__main__":
    main()
