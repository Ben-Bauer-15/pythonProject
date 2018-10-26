from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime
import pytz
import json
from django.core.mail import send_mail

def index(request):
    return render(request, 'signup/index.html')

def signup(request):
    return render(request, 'signup/signup.html')

def new_user(request):
    if request.method == 'POST':
        errors = User.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
            return redirect('/signup')
        
        else:
            if request.POST['mp_email'] != '':

                User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()), mp_username = request.POST['mp_email'])

                id = User.objects.get(email = request.POST['email'])
                request.session['id'] = id
                return redirect('/')
            
            User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
            id = User.objects.get(email = request.POST['email']).id
            request.session['id'] = id
            request.session['name'] = User.objects.get(email = request.POST['email']).first_name
            request.session['loggedin'] = True
            return redirect('/')
    
    else:
        return redirect('/')

def signin(request):
    if request.method == "POST":
        errors = User.objects.login_validation(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)
            return redirect('/login')
        
        else:
            request.session['name'] = User.objects.get(email = request.POST['email']).first_name
            request.session['loggedin'] = True
            request.session['id'] = User.objects.get(email = request.POST['email']).id
            return redirect('/login')
    else:
        return redirect('/')

def process_ajax(request):
    if request.method == "POST":
        errors = User.objects.basic_validation(request.POST)
        print('error at process ajax')
        return HttpResponse(json.dumps(errors), content_type = 'application/json')
    else:
        return redirect('/')


def login(request):
    return render(request, 'signup/signin.html')

def logout(request):
    request.session.clear()
    return redirect('/')

    
def history(request):
    return render(request, 'signup/history.html')

def view(request, id):
    return render(request, 'signup/view.html')

def users(request):
    return render(request, 'signup/user_table.html')

def user(request, id):
    return render(request, 'signup/other_user.html')

def create(request):
    return render(request, 'signup/create_workout.html')

def record(request):
    return render(request, 'signup/log_workout.html')

def add_set(request):
    if request.method == 'POST':

        exercise_number = (request.POST['exercise_adding_to'])
        sets = int(request.POST['exercise_' + exercise_number + '_sets']) + 1
        
        return render(request, 'signup/new_set.html', {'new_set' : sets, 'exercise_number' : exercise_number})
    
    return HttpResponse('blah')

def add_exercise(request):
    if request.method == 'POST':
        num_exercises = int(request.POST['num_exercises'])
        num_exercises += 1
        return render(request, 'signup/new_exercise.html', {'num_exercises' : num_exercises})
        
    return HttpResponse('asfdasdfadsf')

def create_workout(request):
    keys = []
    if request.method == "POST":
        for key in request.POST.keys():
            keys.append(key)
        print(keys)
        return redirect('/create')
    return redirect('/create')