from django import forms
from ..login_reg_app.models import User
from .models import Food
from django.core.exceptions import ValidationError
import bcrypt

class QuickFood(forms.ModelForm):
	class Meta:
		model = Food
		fields = ('food_id',)
	food = forms.CharField(max_length=100)


class QuickWeight(forms.ModelForm):
	class Meta:
		model = User
		fields = ('weight',)
	weight = forms.DecimalField(max_digits=5, decimal_places=1)