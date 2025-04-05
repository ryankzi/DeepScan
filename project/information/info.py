import psutil
import platform

def return_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    cpu_model = platform.processor()



    information = {
        'cpu_usage': f"{cpu_usage}%",
        'ram_usage': f"{ram_percent}%",
        'cpu_model': cpu_model
    }

    return information
