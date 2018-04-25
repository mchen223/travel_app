from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from ..log_reg.models import *
import re
import datetime

destination_regex = re.compile(r'^[a-zA-Z -,.]+$')

class TripManager(models.Manager):
    def add_trip(self, form_data, request):
        valid = True
        user = User.objects.get(username = request.session['username'])
        destination = form_data['destination']
        description = form_data['description']
        date_from = form_data['date_from']
        date_to =form_data['date_to']
        if not destination_regex.match(form_data['destination']):
            messages.warning(request, "Destinations must be comprised of all letters, and no apostrophes!")
            valid = False
        if len(form_data['destination'])<1:
            messages.error(request, "Destination can not be blank. No drifting in the wind!")
            valid = False
        if len(form_data['description'])<1:
            messages.error(request, "Description can not be blank!")
            valid = False
        if not form_data['date_from'] or not form_data['date_to']:
            messages.error(request, "Dates range must be provided. No drifting in the wind!")
            valid = False
        if form_data['date_to'] < form_data['date_from']:
            messages.error(request, "End date can not be before start date!")
            valid = False
        if form_data['date_from'] < str(datetime.date.today()):
            messages.error(request, "Start date can not be before current date. No timeturners here!")
            valid = False
        if valid == True:
            Trip.objects.create(destination=destination, description=description, date_from=date_from, date_to=date_to, user_creator=user)
            print request.session['name'] + " added a trip to " + form_data['destination']
        return valid

    def join(self, id, request):
        print request.session['name'] + " is joining the trip to " + Trip.objects.get(id=id).destination
        this_user = User.objects.get(id=request.session['user_id'])
        this_trip = Trip.objects.get(id=id)
        this_trip.user_joiner.add(this_user)

    def leave_trip(self, id, request):
        print request.session['name'] + " is leaving the trip to " + Trip.objects.get(id=id).destination
        this_user = User.objects.get(id=request.session['user_id'])
        this_trip = Trip.objects.get(id=id)
        this_trip.user_joiner.remove(this_user)

    def delete_trip(self, id, request):
        trip = Trip.objects.get(id=id)
        valid = True
        if not trip.user_creator_id == request.session['user_id']:
            messages.error(request, "You're not the creator of this trip, so you can't delete it. Please email creator for them to remove you manually.")
            valid = False
        else:
            trip.delete()
            print "Sucessfully deleted trip " + id
        return valid

class Trip(models.Model):
    destination = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    user_creator= models.ForeignKey(User, related_name="user_create")
    user_joiner = models.ManyToManyField(User, related_name="user_join")
    objects = TripManager()

    def __str__(self):
        return self.destination
