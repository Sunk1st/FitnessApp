'''

ValidationError allows for registration forms to be validated.

'''

from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models

'''

validateName is the only validator function used that has direct relation to the User.

'''

def validateName(name):
    if len(name) < 3:
        raise ValidationError('Your input, {}, must be longer than 2.'.format(name))
    for a in name:
        if not a.isalpha():
            raise ValidationError('Your input, {}, must be alphabetic.'.format(name))

'''

The range of possible values is extended beyond what is possible/most probable to input.

'''

class User(models.Model):
    first_name = models.CharField(max_length=255, validators = [validateName])
    last_name = models.CharField(max_length=255, validators = [validateName])
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    feet = models.IntegerField()
    inches = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    activity_level = models.DecimalField(max_digits=5, decimal_places=3)
    goal = models.IntegerField()
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)