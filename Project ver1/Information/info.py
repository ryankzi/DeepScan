import psutil

def return_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_percent = ram.percent



    information = {
        'cpu_usage': f"{cpu_usage}%",
        'ram_usage': f"{ram_percent}%",
    }

    return information
