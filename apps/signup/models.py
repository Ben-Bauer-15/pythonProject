from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
from django.utils.timezone import now

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class userManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "This field cannot be blank"
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "Name must be at least two characters"
        elif not postData['first_name'].isalpha():
            errors['first_name'] = "Name must only contain letters"


        if len(postData['last_name']) < 1:
            errors['last_name'] = "This field cannot be blank"
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Name must be at least two characters"
        elif not postData['last_name'].isalpha():
            errors['last_name'] = "Name must only contain letters"
        

        if len(postData['email']) < 1:
            errors['email'] = "This field cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email not valid"
        else:
            users = User.objects.filter(email = postData['email'])
            if len(users) > 0:
                errors['email'] = 'Email already exists in database'

        if len(postData['password']) < 1:
            errors['password'] = "This field cannot be blank"
        elif len(postData['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters long"
        elif postData['password'] != postData['password_confirm']:
            errors['password'] = "Passwords do not match"

        return errors
            

    def login_validation(self, postData):
        users = User.objects.filter(email = postData['email'])
        errors = {}

        if len(postData['email']) < 1:
            errors['address_login'] = "Please fill out this field"
        if len(postData['password']) < 1:
            errors['pw_login'] = "Please fill out this field"
        elif len(users) == 0:
            errors['address_login'] = "Sorry, we could not find this email"
        
        else:
            if not bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                errors['pw_login'] = "Email/password combination does not match"
        return errors

class workoutManager(models.Manager):

    def get_uploaded_workouts(self, user):
        return user.workouts.all()

    def find_workout(self, postData, user):
        workout = user.workouts.get(name = postData['workout_name'])
        return workout
        
    def get_logged_workouts(self, user):
        return user.workouts_logged.all()


    def log_workout(self, user, keys, postData, orig_workout):
        if 'notes' in keys:
            user.workouts_logged.add(
                Workout_Logged.objects.create(
                name = postData['workout_name'],
                notes = postData['notes']
            ))
        else:
            user.workouts_logged.add(
                Workout_Logged.objects.create(
                name = postData['workout_name']
            ))

        # loop through the length of the number of exercises
        num_exercises = len(orig_workout.exercises.all())
        for i in range(num_exercises):
            Exercise_Logged.objects.create(
                name = orig_workout.exercises.all()[i].name,
                resistance = orig_workout.exercises.all()[i].resistance,
                workout = Workout_Logged.objects.last(), 
                exercise_number = i + 1
            )


            #loop through the length of the number of sets in an exercise
            num_sets = len( orig_workout.exercises.all()[i].sets.all() )
            for j in range(num_sets):
                Set_Logged.objects.create(
                    set_number = j + 1,
                    result = postData['exercise_' + str(i + 1) + '_set_' + str(j + 1) + '_result'],
                    exercise = Exercise_Logged.objects.last()
                )
        return True

    def create_workout(self, postData, keys, user):

        if 'description' in keys:
            Workout.objects.create(
                name = postData['workout_name'],
                description = postData['description'],
                uploaded_by = user
            )
            
        else:
            Workout.objects.create(
                name = postData['workout_name'],
                uploaded_by = user
            )
        

        # loop through the length of the number of exercises
        num_exercises = int( postData['num_exercises'] )
        for i in range(1, num_exercises + 1):

            Exercise.objects.create(
                name = postData[ 'exercise_' + str(i) + '_name'],
                resistance = postData[ 'exercise_' + str(i) + '_resistance'],
                workout = Workout.objects.last(), 
                exercise_number = int(i)
            )

            #loop through the length of the number of sets in an exercise
            num_sets = int( postData['exercise_' + str(i) + '_sets'] )
            for j in range(1, num_sets + 1):

                if 'exercise_' + str(i) + '_set_' + str(j) + '_minutes' not in keys:
                    Set.objects.create(
                        reps = postData['exercise_' + str(i) + '_set_' + str(j) + '_reps'],
                        seconds = postData['exercise_' + str(i) + '_set_' + str(j) + '_seconds'],
                        exercise = Exercise.objects.last(), 
                        set_number = int(j)
                    )

                elif 'exercise_' + str(i) + '_set_' + str(j) + '_seconds' not in keys:
                    Set.objects.create(
                        reps = postData['exercise_' + str(i) + '_set_' + str(j) + '_reps'],
                        minutes = postData['exercise_' + str(i) + '_set_' + str(j) + '_minutes'],
                        exercise = Exercise.objects.last(), 
                        set_number = int(j)
                    )
                
                else:
                    Set.objects.create(
                        reps = postData['exercise_' + str(i) + '_set_' + str(j) + '_reps'],
                        minutes = postData['exercise_' + str(i) + '_set_' + str(j) + '_minutes'],
                        seconds = postData['exercise_' + str(i) + '_set_' + str(j) + '_seconds'],
                        exercise = Exercise.objects.last(), 
                        set_number = int(j)
                    )


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    bio = models.TextField(default = '')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    mp_username = models.CharField(max_length = 255, default = '')
    password = models.CharField(max_length = 255)
    objects = userManager()

class Workout(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(default = '')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    uploaded_by = models.ForeignKey(User, related_name = 'workouts', on_delete = models.CASCADE)
    objects = workoutManager()

class Exercise(models.Model):
    name = models.CharField(max_length = 255)
    resistance = models.CharField(max_length = 255)
    workout = models.ForeignKey(Workout, related_name = 'exercises', on_delete = models.CASCADE)
    exercise_number = models.IntegerField(default = 0)

class Set(models.Model):
    seconds = models.IntegerField(default = 0)
    set_number = models.IntegerField(default = 0)
    minutes = models.IntegerField(default = 0)
    reps = models.IntegerField(default = 0)
    result = models.IntegerField(default = 0)
    notes = models.TextField(default = '')
    exercise = models.ForeignKey(Exercise, related_name = 'sets', on_delete = models.CASCADE)

class Workout_Logged(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(default = '')
    logged_at = models.DateTimeField(auto_now_add = True)
    users_logged = models.ManyToManyField(User, related_name = 'workouts_logged')
    notes = models.TextField(default = '')
    objects = workoutManager()

class Exercise_Logged(models.Model):
    name = models.CharField(max_length = 255)
    resistance = models.CharField(max_length = 255)
    workout = models.ForeignKey(Workout_Logged, related_name = 'exercises', on_delete = models.CASCADE)
    exercise_number = models.IntegerField(default = 0)

class Set_Logged(models.Model):
    set_number = models.IntegerField(default = 0)
    result = models.IntegerField(default = 0)
    exercise = models.ForeignKey(Exercise_Logged, related_name = 'sets', on_delete = models.CASCADE)
    