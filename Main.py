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

def refresh_info():
    text_area.delete('1.0', tk.END)
    info = (
        get_system_info() + "\n" +
        get_cpu_info() + "\n" +
        get_memory_info() + "\n" +
        get_disk_info()
    )
    text_area.insert(tk.END, info)

# Setup GUI
root = tk.Tk()
root.title("Hardware Info Monitor")
root.geometry("700x600")

text_area = ScrolledText(root, font=("Consolas", 10))
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

refresh_button = tk.Button(root, text="Refresh", command=refresh_info)
refresh_button.pack(pady=5)

# Load info on startup
refresh_info()

root.mainloop()
