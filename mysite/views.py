from django.shortcuts import render, redirect
import requests
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, 'mysite/index.html')