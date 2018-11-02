from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime
import pytz
import json
from django.core.mail import send_mail
import requests

def index(request):
    return render(request, 'signup/index.html')

def signup(request):
    return render(request, 'signup/signup.html')

# def find_ticks(request, id):
#     response = requests.get('https://www.mountainproject.com/data/get-ticks?email=benjaminbauer15@gmail.com&key=110693748-ed3e51ce6c9ba16b8305073256fadc9b')
#     ticks = reponse.json()

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

                id = User.objects.get(email = request.POST['email']).id
                request.session['id'] = id
                return redirect('/')
            
            User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
            id = User.objects.get(email = request.POST['email']).id
            request.session['id'] = id
            request.session['name'] = User.objects.get(email = request.POST['email']).first_name
            request.session['loggedin'] = True
            return redirect('/history')
    
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
            return redirect('/history')
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
    user = User.objects.get(id = request.session['id'])
    workouts = Workout.objects.get_logged_workouts(user)

    return render(request, 'signup/history.html', {'workouts' : workouts})

def view(request, id):
    workout = Workout_Logged.objects.get(id = id)
    return render(request, 'signup/view.html', {'workout' : workout})

def delete(request, id):
    
    Workout_Logged.objects.get(id = id).delete()

    user = User.objects.get(id = request.session['id'])
    workouts = Workout.objects.get_logged_workouts(user)

    return render(request, 'signup/ajax_delete_workout.html', {'workouts' : workouts})

def update(request, workout_id, exercise_id, set_id):
    my_key = 0
    for key in request.GET.keys():
        my_key = key
    workout = Workout_Logged.objects.get(id = workout_id)
    exercise = workout.exercises.get(exercise_number = exercise_id)
    set_number = exercise.sets.get(set_number = set_id)
    set_number.result = int(my_key)
    set_number.save()
    exercise.save()
    workout.save()
    return HttpResponse('asdfasdf')

def users(request):
    users = User.objects.all()
    me = User.objects.get(id = request.session['id'])
    contributions = {}
    for user in users:
        contributions[user] = len(user.workouts.all())
    return render(request, 'signup/user_table.html', {'users' : users, 'me' : me, 'contributions' : contributions})

def user(request, id):
    user = User.objects.get(id = id)
    workouts = len(user.workouts.all())
    if user.mp_username != '':
        response = requests.get('https://www.mountainproject.com/data/get-ticks?email=' + str(user.mp_username) + '&key=110693748-ed3e51ce6c9ba16b8305073256fadc9b')
        ticks = response.json()
        ticks = ticks['ticks']
        ticks = ticks[:10]
        my_routes ={}
        query = ''
        for route in ticks:
            query += str(route['routeId'])
            query += ','
        query = query[:len(query) - 1]

        response = requests.get('https://www.mountainproject.com/data/get-routes?routeIds=' + str(query) + '&key=110693748-ed3e51ce6c9ba16b8305073256fadc9b')
        route_data = response.json()
        routes = route_data['routes'][:10]

        return render(request, 'signup/other_user.html', {'user': user, 'workouts' : workouts, 'routes' : routes})
    
    else:
        return render(request, 'signup/other_user.html', {'user': user, 'workouts' : workouts})

def log_friend_workout(request, id):
    friend_workout = Workout.objects.get(id = id)
    print(friend_workout.name)
    return render(request, 'signup/log_workout.html', {'friend_workout' : friend_workout})

def create(request):
    return render(request, 'signup/create_workout.html')

def record(request):
    user =  User.objects.get(id = request.session['id'])
    workouts = Workout.objects.get_uploaded_workouts(user)
    return render(request, 'signup/log_workout.html', {'workouts' : workouts})

def find_workout(request):
    if request.method == 'POST':
        user = User.objects.get(id = request.session['id'])
        workout = Workout.objects.find_workout(request.POST, user)
        return render(request, 'signup/ajax_workout.html', {'workout' : workout})
    
    return HttpResponse('blah')

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
        user = User.objects.get(id = request.session['id'])
        Workout.objects.create_workout(request.POST, keys, user)
        return redirect('/record')
    return redirect('/create')

def record_workout(request):
    keys = []
    if request.method == "POST":
        for key in request.POST.keys():
            keys.append(key)

        user = User.objects.get(id = request.session['id'])
        orig_workout = Workout.objects.get(name = request.POST['workout_name'])
        Workout_Logged.objects.log_workout(user, keys, request.POST, orig_workout)

        return redirect('/history')

    return redirect('/')