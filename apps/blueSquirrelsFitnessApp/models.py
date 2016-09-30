from __future__ import unicode_literals
from ..login_reg_app.models import User
from django.db import models

class Food(models.Model):
	food = models.CharField(max_length=255)
	quantity = models.DecimalField(default=1, max_digits=4, decimal_places=2)
	calories = models.DecimalField(default=0, max_digits=7, decimal_places=2)
	carbohydrates = models.DecimalField(default=0, max_digits=7, decimal_places=2)
	lipids = models.DecimalField(default=0, max_digits=7, decimal_places=2)
	protein = models.DecimalField(default=0, max_digits=7, decimal_places=2)
	sugar = models.DecimalField(default=0, max_digits=5, decimal_places=2)
	user = models.ForeignKey(User)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)