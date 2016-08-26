from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Count
# from models import User, Poke
import bcrypt
# from datetime import date

def index(request):
    return render(request, 'travel_plan/index.html')

def user(request):
    return render(request, 'travel_plan/user.html')

def travel(request):
    return render(request, 'travel_plan/travel.html')

def add(request):
    return render(request, 'travel_plan/add.html')
