from django.urls import path
from . import views

urlpatterns = [
    path('information/', views.system_info, name='system_info')
]