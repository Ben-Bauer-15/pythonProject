from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from datetime import datetime
import pytz
import json
from django.core.mail import send_mail

def index(request):
    return render(request, 'signup/index.html')

def signup(request):
    return render(request, 'signup/signup.html')

def create(request):
    return render(request, 'signup/create_workout.html')

def add_set(request):
    if request.method == 'POST':
        new_set = int(request.POST['set']) + 1
        return render(request, 'signup/new_set.html', {'new_set' : new_set})
    return HttpResponse('asfdasdfadsf')

# def send_mail(request):
#     if request.method == 'POST':
#         print(request.POST)
#         send_mail('Subject', 'Message', 'benjaminbauer15@gmail.com', [request.POST['search']])
#         return redirect('/')
#     else:
#         return redirect('/')