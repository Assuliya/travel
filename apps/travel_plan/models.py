from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')

class UserManager(models.Manager):
    def validateReg(self, request):
        errors = []
        if len(request.POST['name']) < 3:
            errors.append('Name can not be less than 3 characters')
        elif not all(x.isalpha() or x.isspace() for x in request.POST['name']):
            errors.append('Name should only contain letters')
        if len(request.POST['alias']) < 3:
            errors.append('Username can not be less than 3 characters')
        try:
            user = User.objects.get(alias = request.POST['alias'])
            errors.append('This alias is already being used')
        except ObjectDoesNotExist:
            pass
        if len(errors) > 0:
            return (False, errors)
        return (True, errors)

    def validateRegPass(self, request):
        errors = []
        if len(request.POST['password']) < 1:
            errors.append('Password can not be empty')
        elif len(request.POST['password']) < 8:
            errors.append('Password should be more than 7 characters')
        elif not PASS_REGEX.match(request.POST['password']):
            errors.append('Password should contain at least one apper case letter and one number')
        if request.POST['password'] != request.POST['repeat']:
            errors.append('Password repeat did not match the password')
        if len(errors) > 0:
            return (False, errors)
        return (True, errors)

    def validateLogin(self, request):
        from bcrypt import hashpw, gensalt
        errors = []
        try:
	        user = self.get(alias=request.POST['alias'])
	        password = user.pw_hash.encode()
	        loginpass = request.POST['password'].encode()
	        if hashpw(loginpass, password) == password:
	            return (True, user)
	        else:
	            errors.append("Sorry, no password match. Please try again.")
	            return (False, errors)
        except ObjectDoesNotExist:
            pass
        errors.append("Sorry, no username found. Please try again.")
        return (False, errors)


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()
    manager = UserManager()

class Travel(models.Model):
      destination = models.CharField(max_length=255)
      plan = models.TextField(max_length=500)
      start = models.DateField()
      end = models.DateField()
      user_id = models.ForeignKey(User, related_name='travel_create')
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

class Join(models.Model):
      travel_id = models.ForeignKey(Travel, related_name='join_travel')
      user_id = models.ForeignKey(User, related_name='join_user')
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
