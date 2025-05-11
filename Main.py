import platform
import os
import psutil
import cpuinfo

def get_system_info():
    print("=== System Information ===")
    print(f"System: {platform.system()}")
    print(f"Node Name: {platform.node()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Architecture: {' '.join(platform.architecture())}")

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    print("\n=== CPU Info ===")
    print(f"Brand: {info.get('brand_raw', 'N/A')}")
    print(f"Cores (logical): {psutil.cpu_count(logical=True)}")
    print(f"Cores (physical): {psutil.cpu_count(logical=False)}")
    print(f"Frequency: {psutil.cpu_freq().current:.2f} MHz")

def get_memory_info():
    mem = psutil.virtual_memory()
    print("\n=== Memory Info ===")
    print(f"Total: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Available: {mem.available / (1024 ** 3):.2f} GB")
    print(f"Used: {mem.used / (1024 ** 3):.2f} GB")

def get_disk_info():
    print("\n=== Disk Info ===")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Device: {partition.device}")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            print(f"  Total Size: {usage.total / (1024 ** 3):.2f} GB")
            print(f"  Used: {usage.used / (1024 ** 3):.2f} GB")
            print(f"  Free: {usage.free / (1024 ** 3):.2f} GB")
        except PermissionError:
            continue


get_system_info()
get_cpu_info()
get_memory_info()
get_disk_info()
