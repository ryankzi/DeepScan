import platform
import os
import psutil
import cpuinfo
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess

def get_system_info():
    info = []
    info.append("=== System Information ===")
    info.append(f"System: {platform.system()}")
    info.append(f"Node Name: {platform.node()}")
    info.append(f"Release: {platform.release()}")
    info.append(f"Version: {platform.version()}")
    info.append(f"Machine: {platform.machine()}")
    info.append(f"Processor: {platform.processor()}")
    info.append(f"Architecture: {' '.join(platform.architecture())}")
    return "\n".join(info)

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    cpu = []
    cpu.append("\n=== CPU Info ===")
    cpu.append(f"Brand: {info.get('brand_raw', 'N/A')}")
    cpu.append(f"Cores (logical): {psutil.cpu_count(logical=True)}")
    cpu.append(f"Cores (physical): {psutil.cpu_count(logical=False)}")
    freq = psutil.cpu_freq()
    if freq:
        cpu.append(f"Frequency: {freq.current:.2f} MHz")
    return "\n".join(cpu)

def get_memory_info():
    mem = psutil.virtual_memory()
    meminfo = []
    meminfo.append("\n=== Memory Info ===")
    meminfo.append(f"Total: {mem.total / (1024 ** 3):.2f} GB")
    meminfo.append(f"Available: {mem.available / (1024 ** 3):.2f} GB")
    meminfo.append(f"Used: {mem.used / (1024 ** 3):.2f} GB")
    return "\n".join(meminfo)

def get_disk_info():
    disks = []
    disks.append("\n=== Disk Info ===")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append(f"Device: {partition.device}")
            disks.append(f"  Mountpoint: {partition.mountpoint}")
            disks.append(f"  File system type: {partition.fstype}")
            disks.append(f"  Total Size: {usage.total / (1024 ** 3):.2f} GB")
            disks.append(f"  Used: {usage.used / (1024 ** 3):.2f} GB")
            disks.append(f"  Free: {usage.free / (1024 ** 3):.2f} GB")
        except PermissionError:
            continue
    return "\n".join(disks)

def get_gpu_info():
    gpus = []
    gpus.append("\n=== GPU Info ===")
    
    # Try GPUtil first
    try:
        import GPUtil
        try:
            gpu_list = GPUtil.getGPUs()
            if not gpu_list:
                gpus.append("No GPUs detected by GPUtil")
            else:
                for i, gpu in enumerate(gpu_list):
                    gpus.append(f"GPU {i+1}: {gpu.name}")
                    gpus.append(f"  Driver: {gpu.driver}")
                    gpus.append(f"  Memory Total: {gpu.memoryTotal} MB")
                    gpus.append(f"  Memory Free: {gpu.memoryFree} MB")
                    gpus.append(f"  Memory Used: {gpu.memoryUsed} MB")
                    gpus.append(f"  Temperature: {gpu.temperature} °C")
                return "\n".join(gpus)
        except Exception as e:
            gpus.append(f"GPUtil error: {str(e)}")
    except ImportError:
        gpus.append("GPUtil not installed (pip install gputil)")
    
    # Try alternative methods if GPUtil fails
    if platform.system() == "Windows":
        try:
            import wmi
            w = wmi.WMI()
            for gpu in w.Win32_VideoController():
                gpus.append(f"GPU: {gpu.Name}")
                if hasattr(gpu, 'AdapterRAM'):
                    ram_gb = int(gpu.AdapterRAM) / (1024 ** 3)
                    gpus.append(f"  Memory: {ram_gb:.2f} GB")
                if hasattr(gpu, 'DriverVersion'):
                    gpus.append(f"  Driver Version: {gpu.DriverVersion}")
            return "\n".join(gpus)
        except Exception as e:
            gpus.append(f"WMI error: {str(e)}")
    elif platform.system() == "Linux":
        try:
            # Try to get GPU info from lspci if available
            if os.path.exists('/usr/bin/lspci'):
                lspci_output = os.popen('lspci -nn | grep -i vga').read()
                if lspci_output:
                    gpus.append("GPUs detected:")
                    for line in lspci_output.split('\n'):
                        if line.strip():
                            gpus.append(f"  {line.strip()}")
                else:
                    gpus.append("No GPUs detected by lspci")
            else:
                gpus.append("lspci not available")
            return "\n".join(gpus)
        except Exception as e:
            gpus.append(f"Linux GPU detection error: {str(e)}")
    
    if len(gpus) <= 1:  # Only has the header
        gpus.append("Could not detect GPU information")
    
    return "\n".join(gpus)

def get_drivers_info():
    drivers_info = "\n=== Drivers Info ==="
    if platform.system() == "Windows":
        try:
            drivers = subprocess.check_output("driverquery /FO LIST", shell=True).decode()
            drivers_info += "\n" + drivers
        except subprocess.CalledProcessError:
            drivers_info += "\nFailed to fetch drivers information."
    elif platform.system() == "Linux":
        try:
            drivers = subprocess.check_output("lspci -v", shell=True).decode()
            drivers_info += "\n" + drivers
        except subprocess.CalledProcessError:
            drivers_info += "\nFailed to fetch drivers information."
    else:
        drivers_info += "\nDrivers info not supported on this platform."
    return drivers_info

def get_motherboard_info():
    try:
        if platform.system() == "Windows":
            import wmi
            w = wmi.WMI()
            mobo_info = []
            mobo_info.append("\n=== Motherboard Info ===")
            
            for board in w.Win32_BaseBoard():
                mobo_info.append(f"Manufacturer: {board.Manufacturer}")
                mobo_info.append(f"Product: {board.Product}")
                mobo_info.append(f"Serial Number: {board.SerialNumber}")
                mobo_info.append(f"Version: {board.Version}")
            
            for bios in w.Win32_BIOS():
                mobo_info.append(f"BIOS Vendor: {bios.Manufacturer}")
                mobo_info.append(f"BIOS Version: {bios.Version}")
                mobo_info.append(f"BIOS Date: {bios.ReleaseDate}")
            
            return "\n".join(mobo_info)
        else:
            mobo_info = []
            mobo_info.append("\n=== Motherboard Info ===")
            
            if platform.system() == "Linux":
                try:
                    with open('/sys/devices/virtual/dmi/id/board_vendor', 'r') as f:
                        mobo_info.append(f"Manufacturer: {f.read().strip()}")
                    with open('/sys/devices/virtual/dmi/id/board_name', 'r') as f:
                        mobo_info.append(f"Product: {f.read().strip()}")
                    with open('/sys/devices/virtual/dmi/id/board_serial', 'r') as f:
                        mobo_info.append(f"Serial Number: {f.read().strip()}")
                    with open('/sys/devices/virtual/dmi/id/board_version', 'r') as f:
                        mobo_info.append(f"Version: {f.read().strip()}")
                except FileNotFoundError:
                    mobo_info.append("DMI information not available")
            else:
                mobo_info.append("Motherboard information requires Windows or Linux")
            
            return "\n".join(mobo_info)
    except ImportError:
        return "\n=== Motherboard Info ===\nwmi library not installed (Windows only). Install with 'pip install wmi'"
    except Exception as e:
        return f"\n=== Motherboard Info ===\nError getting motherboard info: {str(e)}"

def refresh_info():
    text_area.delete('1.0', tk.END)
    info = (
        get_system_info() + "\n" +
        get_cpu_info() + "\n" +
        get_memory_info() + "\n" +
        get_disk_info() + "\n" +
        get_gpu_info() + "\n" +
        get_motherboard_info() + "\n" + 
        get_drivers_info()
    )
    text_area.insert(tk.END, info)

# Setup GUI
root = tk.Tk()
root.title("DeepScan")
root.geometry("1920x1080")
root.state("zoomed")

text_area = ScrolledText(root, font=("Consolas", 10))
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

refresh_button = tk.Button(root, text="Refresh", command=refresh_info)
refresh_button.pack(pady=5)

# Load info on startup
refresh_info()

root.mainloop()
