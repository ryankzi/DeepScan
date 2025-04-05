from information.info import return_info
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse



def system_info(request):
    template = loader.get_template('site.html')

    data = return_info()


    return HttpResponse(template.render(data, request))