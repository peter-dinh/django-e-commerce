from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from .models import *

def index(request):
    
    return render(request, 'app/index.html')

def login(request):
    return render(request, 'app/login.html')

def register(request):
    return render(request, 'app/register.html')

def cart(request):
    return render(request, 'app/cart.html')

def info(request):
    return render(request, 'app/product-details.html')

def catalog(request):
    return render(request, 'app/shop.html')

def account(request):
    return render(request, 'app/shop.html')

def bill(request):
    return render(request, 'app/shop.html')

def change_pass(request):
    return render(request, 'app/shop.html')