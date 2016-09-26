from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models

def validateName(name):
    if len(name) < 3:
        raise ValidationError('{} must be longer than 2.'.format(name))
    for a in name:
        if not a.isalpha():
            raise ValidationError('{} must be alphabetic.'.format(name))



class User(models.Model):
    first_name = models.CharField(max_length=255, validators = [validateName])
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    height = models.IntegerField()
    weight = models.DecimalField(max_digits=3, decimal_places=1)
    password = models.CharField(max_length=255)