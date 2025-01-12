# Linux System Report Generator

This Python script collects system information and installed packages on a Linux machine and generates an Excel report. It is useful for system administrators who need to gather detailed system and package information.

---

## Features

- Collects detailed system information such as:
  - Operating System, Kernel version, CPU, RAM, and disk usage,
  - Uptime and Python version,
  - List of superusers with `sudo` rights,
- Lists installed packages on the system (supports `yum` and `dnf` package managers).
- Generates a detailed report in Excel format with two sheets:
  - **System Info**: Key-value pairs of system details
  - **Installed Packages**: List of installed packages on the system
- Adjusts column widths and adds borders for better readability in the Excel file.
- Centers the text in all cells of the Excel report.


## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `psutil==5.8.0`
  - `pandas==2.2.3`
  - `openpyxl==3.1.5`
  
To install the required dependencies, run:

```bash
sudo pip install -r requirements.txt
```


## Script Execution
This script needs to be executed with sudo privileges, as it requires access to system-level information (e.g., packages, system details, superusers).

To run the script:

```python
sudo python3 LinuxSystemReportGenerator.py
```
The script will generate an Excel file named `system_info.xlsx` containing the system information and installed packages.



## License
This project is licensed under the MIT License.


## Acknowledgements
The system information is collected using the `psutil` and platform libraries.
Excel handling and styling is done using the `openpyxl` library.
Special thanks to the Python community for their open-source contributions.