import psutil
import cpuinfo


def return_info():
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Get RAM usage
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    
    # Get CPU model information
    cpu = cpuinfo.get_cpu_info()
    cpu_model = cpu.get('brand_raw', 'Unknown CPU Model')  # Using 'brand_raw' as it's more consistent
    
    # Return information in a dictionary
    information = {
        'cpu_usage': f"{cpu_usage}%",
        'ram_usage': f"{ram_percent}%",
        'cpu_model': cpu_model
    }

    return information
