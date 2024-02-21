from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'users/index.html')

def login(request):
    return render(request,'users/login.html')

def uper(request):
    return render(request,'users/uper.html')

# @login_required
def dashboard(request):
    return render(request,'users/dashboard.html')