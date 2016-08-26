from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Count
from models import User, Travel, Join
import bcrypt
from datetime import date

def index(request):
    return render(request, 'travel_plan/index.html')

def user(request):
    user = User.objects.get(id = request.session['user'])
    other = Travel.objects.all().order_by('start')
    travels = Travel.objects.filter(user_id = request.session['user'])

    joins = Join.objects.filter(user_id = request.session['user'])

    

    context = {'travels':travels, 'user':user, 'other':other, 'joins': joins}
    return render(request, 'travel_plan/user.html', context)

def travel(request, travel_id):
    travel = Travel.objects.get(id = travel_id)
    context = {'travel':travel}
    return render(request, 'travel_plan/travel.html', context)

def add(request):
    today = date.today()
    format_time = today.strftime('%Y-%m-%d')
    context = {'time':format_time}
    return render(request, 'travel_plan/add.html', context)




def register_process(request):
    result = User.manager.validateReg(request)
    resultPass = User.manager.validateRegPass(request)
    if result[0] == False or resultPass[0] == False:
        errors = result[1]+resultPass[1]
        print_messages(request, errors)
        return redirect(reverse('index'))
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.manager.create(name=request.POST['name'], alias=request.POST['alias'], pw_hash=pw_hash)
    return log_user_in(request, user)

def login_process(request):
    result = User.manager.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('index'))
    return log_user_in(request, result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def log_user_in(request, user):
    request.session['user'] = user.id
    return redirect(reverse('user'))

def logout(request):
    user = User.manager.get(id=request.session['user'])
    request.session.pop('user')
    return redirect(reverse('index'))

def add_travel(request):
    errors = []
    print request.POST['end']
    if len(request.POST['destination']) < 1:
        errors.append('Destination can not be empty')
    if len(request.POST['plan']) < 1:
        errors.append('Plan can not be empty')
    if len(request.POST['start']) < 1:
        errors.append('Travel Date From can not be empty')
    if len(request.POST['end']) < 1:
        errors.append('Travel Date To can not be empty')
    if request.POST['end'] < request.POST['start']:
        errors.append('Travel Date To can not be earlier than Travel Date From')
    if len(errors) > 0:
        print errors
        print_messages(request, errors)
        return redirect(reverse('add'))
    creator = User.objects.get(id = request.session['user'])
    travel = Travel.objects.create(user_id_join = creator, user_id = creator, destination=request.POST['destination'], plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'])
    return redirect(reverse('user'))

def join(request, travel_id):

    user = User.objects.get(id = request.session['user'])
    travel = User.objects.get(id = request.session['user'])

    join = Join.objects.create(travel_id = travel, user_id = user)

    return redirect(reverse('user'))
