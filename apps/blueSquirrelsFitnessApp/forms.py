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
	activity_level = forms.ChoiceField(widget=forms.Select, choices=(('1.2', 'Sedentary'), ('1.375', 'Low-Intensity'), ('1.55', 'Medium-Intensity'), ('1.725', 'High-Intensity'), ('1.9', 'Extreme-Intensity')))

class QuickGoal(forms.ModelForm):
	class Meta:
		model = User
		fields = ('goal',)
	goal = forms.ChoiceField(widget=forms.Select, choices=(('-1000', 'Lose 2 Pounds'), ('-500', 'Lose 1 Pound'), ('0', 'Maintain'), ('500', 'Gain 1 Pound'), ('1000', 'Gain 2 Pounds')))