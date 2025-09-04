from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    """Главная страница приложения server"""
    return HttpResponse("Server app is working! 🚀")