from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Django server is working!")

urlpatterns = [
    path('', home_view),
]