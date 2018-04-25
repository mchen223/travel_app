from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib import messages

def home(request):
    if not 'name' in request.session:
        return redirect('users:index')
    else:
        context = {
            'my_trips_created':Trip.objects.filter(user_creator=request.session['user_id']),
            'my_trips_joined':Trip.objects.filter(user_joiner=request.session['user_id']),
            'other_trips':Trip.objects.exclude(user_creator=request.session['user_id']).exclude(user_joiner=request.session['user_id']).order_by('date_from')
        }
        return render(request, 'schedules/home.html', context)

def add(request):
    if not 'name' in request.session:
        return redirect('users:index')
    else:
        return render(request, 'schedules/add.html')

def add_trip(request):
    if not 'name' in request.session:
        return redirect('users:index')
    else:
        if Trip.objects.add_trip(request.POST, request):
            valid = True
            print "Successful in adding trip to " + request.POST['destination']
            return redirect(reverse('schedules:home'))
        else:
            valid = False
            print "Unsuccessful in adding trip to " + request.POST['destination']
            return redirect(reverse('schedules:add'))

def join(request, id):
    if not 'name' in request.session:
        return redirect('users:index')
    Trip.objects.join(id, request)
    print request.session['name'] + " is joining the trip"
    return redirect(reverse('schedules:home'))

def destination(request, id):
    if not 'name' in request.session:
        return redirect('users:index')
    else:
        context = {
            'trips':Trip.objects.filter(id=id),
        }
        return render(request, 'schedules/destinations.html', context)

def leave_trip(request, id):
    if not 'name' in request.session:
        return redirect('users:index')
    Trip.objects.leave_trip(id, request)
    return redirect(reverse('schedules:home'))


def delete_trip(request, id):
    if not 'name' in request.session:
        return redirect('users:index')
    else:
        if Trip.objects.delete_trip(id, request):
            valid = True
            print "Deleting trip " + id
        else:
            print "Unable to delete trip " + id
    return redirect(reverse('schedules:home'))
