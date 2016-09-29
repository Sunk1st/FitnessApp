from django import forms
from ..login_reg_app.models import User
from django.core.exceptions import ValidationError
import bcrypt

class QuickWeight(forms.ModelForm):
	class Meta:
		model = User
		fields = ('weight',)
	weight = forms.DecimalField(max_digits=5, decimal_places=1)

class QuickActivity(forms.ModelForm):
	class Meta:
		model = User
		fields = ('activity_level',)
	activity_level = forms.IntegerField()

class QuickGoal(forms.ModelForm):
	class Meta:
		model = User
		fields = ('goal',)
	activity_level = forms.CharField(max_length=255)