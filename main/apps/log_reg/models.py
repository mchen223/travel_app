from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z -]+[\s]+[a-zA-Z -]+$')

class UserManager(models.Manager):
    def valid_registration(self, user_info, request):
        print "Validating information for " + user_info['username']
        valid = True
        if not name_regex.match(user_info['name']):
            messages.warning(request, "Full names must be comprised of all letters, a space between first and last name, and no apostrophes!")
            valid = False
        if len(user_info['name']) < 3:
            messages.warning(request, "Full name must be 3 or more characters long!")
            valid = False
        if not EMAIL_REGEX.match(user_info['username']):
            messages.warning(request, "Email is not a valid email!")
            valid = False
        if len(user_info['username']) < 3:
            messages.warning(request, "Email should be at least 3 characters!")
            valid = False
        if len(user_info['password']) < 8:
            messages.warning(request, "Password is too short!")
            valid = False
        if user_info['password'] != user_info['confirm_password']:
            messages.warning(request, "Passwords do not match!")
            valid = False
        if User.objects.filter(username = user_info['username']):
            messages.error(request, "This username already exists!")
            valid = False
        if valid == True:
            print "Successful registration for " + user_info['username']
            hashed = bcrypt.hashpw(user_info['password'].encode(), bcrypt.gensalt())
            User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed)
        return valid

    def login_user(self, user_info, request):
        print "Validating login information for " + user_info['username']
        valid = True
        if User.objects.filter(username = user_info['username']):
            hashed = User.objects.get(username = user_info['username']).password
            hashed = hashed.encode('utf-8')
            password = user_info['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
                print "Login successful for " + user_info['username']
                valid = True
            else:
                messages.warning(request, "Password does not match the one on file!")
                valid = False
        else:
            messages.warning(request, "Username does not match with one on file!")
            valid = False
        return valid

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name
