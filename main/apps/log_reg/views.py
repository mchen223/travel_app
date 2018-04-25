from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

def index(request):
    if 'name' not in request.session:
        return render(request, 'log_reg/index.html')
    else:
        return redirect(reverse('schedules:home'))

def register(request):
    if User.objects.valid_registration(request.POST, request):
        valid = True
        user = User.objects.get(username = request.POST['username'])
        request.session['name'] = user.name
        request.session['username'] = user.username
        request.session['user_id'] = user.id
        return redirect(reverse('schedules:home'))
    else:
        valid = False
        return redirect(reverse('users:index'))

def login(request):
    if User.objects.login_user(request.POST, request):
        valid = True
        user = User.objects.get(username = request.POST['username'])
        request.session['name'] = user.name
        request.session['username'] = user.username
        request.session['user_id'] = user.id
        return redirect(reverse('schedules:home'))
    else:
        valid = False
        return redirect(reverse('users:index'))

def logout(request):
    print "Logging off " + request.session['username']
    request.session.clear()
    return redirect(reverse('users:index'))
