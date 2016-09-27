from __future__ import unicode_literals
from ..login_reg_app.models import User
from django.db import models

class Food(models.Model):
	food_id = models.IntegerField()
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)