from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models

def validateName(name):
    if len(name) < 3:
        raise ValidationError('Your input, {}, must be longer than 2.'.format(name))
    for a in name:
        if not a.isalpha():
            raise ValidationError('Your input, {}, must be alphabetic.'.format(name))

def validatePass(password):
    if len(password) < 8:
        raise ValidationError('Password is too short!')

class User(models.Model):
    first_name = models.CharField(max_length=255, validators = [validateName])
    last_name = models.CharField(max_length=255, validators = [validateName])
    email = models.EmailField()
    feet = models.IntegerField()
    inches = models.IntegerField()
    weight = models.DecimalField(max_digits=3, decimal_places=1)
    age = models.IntegerField()
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)