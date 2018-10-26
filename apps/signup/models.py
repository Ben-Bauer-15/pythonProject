from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

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
    def create_workout(self, postData):
        pass


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    mp_username = models.CharField(max_length = 255, default = '')
    password = models.CharField(max_length = 255)
    objects = userManager()

class Workout(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(default = '')
    uploaded_by = models.ForeignKey(User, related_name = 'workouts', on_delete = models.CASCADE)
    users_logged = models.ManyToManyField(User, related_name = 'workouts_logged')

class Exercise(models.Model):
    name = models.CharField(max_length = 255)
    resistance = models.CharField(max_length = 255)
    workout = models.ForeignKey(Workout, related_name = 'exercises', on_delete = models.CASCADE)

class Set(models.Model):
    seconds = models.IntegerField(default = 0)
    minutes = models.IntegerField(default = 0)
    reps = models.IntegerField()
    result = models.IntegerField(default = '')
    notes = models.TextField()
    exercise = models.ForeignKey(Exercise, related_name = 'sets', on_delete = models.CASCADE)




    


    


    