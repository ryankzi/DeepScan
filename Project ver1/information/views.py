import psutil
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse



def system_info(request):
    template = loader.get_template('site.html')
    battery = psutil.sensors_battery()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()


    data = {
        'battery': f"{battery}%",
        'cpu_usage': f"{cpu_usage}%",
        'ram_usage': f"{ram.percent}%",
    }


    return HttpResponse(template.render(data, request))