import platform
import os
import psutil
import cpuinfo
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

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
    try:
        import GPUtil
        gpus = []
        gpus.append("\n=== GPU Info ===")
        gpu_list = GPUtil.getGPUs()
        if not gpu_list:
            gpus.append("No GPUs detected")
            return "\n".join(gpus)
            
        for i, gpu in enumerate(gpu_list):
            gpus.append(f"GPU {i+1}: {gpu.name}")
            gpus.append(f"  Driver: {gpu.driver}")
            gpus.append(f"  Memory Total: {gpu.memoryTotal} MB")
            gpus.append(f"  Memory Free: {gpu.memoryFree} MB")
            gpus.append(f"  Memory Used: {gpu.memoryUsed} MB")
            gpus.append(f"  Temperature: {gpu.temperature} °C")
        return "\n".join(gpus)
    except ImportError:
        return "\n=== GPU Info ===\nGPUtil library not installed. Install with 'pip install gputil'"
    except Exception as e:
        return f"\n=== GPU Info ===\nError getting GPU info: {str(e)}"

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
        get_motherboard_info()
    )
    text_area.insert(tk.END, info)

root = tk.Tk()
root.title("Hardware Info Monitor")
root.geometry("1260x720")

text_area = ScrolledText(root, font=("Consolas", 10))
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

refresh_button = tk.Button(root, text="Refresh", command=refresh_info)
refresh_button.pack(pady=5)
refresh_info()

root.mainloop()
