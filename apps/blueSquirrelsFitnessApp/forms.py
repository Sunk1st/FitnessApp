from django import forms
from ..login_reg_app.models import User
from .models import Food
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
	def __init__(self, *args, **kwargs):
		level = kwargs.pop('level')
		super(QuickActivity, self).__init__(*args, **kwargs)
		if level == 1.200:
			self.fields['activity_level'].initial = 1.2
		elif level == 1.375:
			self.fields['activity_level'].initial = 1.375
		elif level == 1.550:
			self.fields['activity_level'].initial = 1.55
		elif level == 1.725:
			self.fields['activity_level'].initial = 1.725
		elif level == 1.900:
			self.fields['activity_level'].initial = 1.9
	activity_level = forms.ChoiceField(widget=forms.Select(), choices=([('1.2', 'Sedentary'), ('1.375', 'Low-Intensity'), ('1.55', 'Medium-Intensity'), ('1.725', 'High-Intensity'), ('1.9', 'Extreme-Intensity')]))

class QuickGoal(forms.ModelForm):
	class Meta:
		model = User
		fields = ('goal',)
	def __init__(self, *args, **kwargs):
		goal = kwargs.pop('goal')
		super(QuickGoal, self).__init__(*args, **kwargs)
		if goal == -1000:
			self.fields['goal'].initial = -1000
		elif goal == -500:
			self.fields['goal'].initial = -500
		elif goal == 0:
			self.fields['goal'].initial = 0
		elif goal == 500:
			self.fields['goal'].initial = 500
		elif goal == 1000:
			self.fields['goal'].initial = 1000
	goal = forms.ChoiceField(widget=forms.Select, choices=(('-1000', 'Lose 2 Pounds'), ('-500', 'Lose 1 Pound'), ('0', 'Maintain'), ('500', 'Gain 1 Pound'), ('1000', 'Gain 2 Pounds')))

class QuantForm(forms.ModelForm):
	class Meta:
		model = Food
		fields = ('quantity',)
	def __init__(self, *args, **kwargs):
		quantity = kwargs.pop('quantity')
		super(QuantForm, self).__init__(*args, **kwargs)
		if quantity == 0.25:
			self.fields['quantity'].initial = 0.25
		elif quantity == 0.5:
			self.fields['quantity'].initial = 0.5
		elif quantity == 0.75:
			self.fields['quantity'].initial = 0.75
		elif quantity == 1:
			self.fields['quantity'].initial = 1
		elif quantity == 2:
			self.fields['quantity'].initial = 2
		elif quantity == 3:
			self.fields['quantity'].initial = 3
		elif quantity == 4:
			self.fields['quantity'].initial = 4
	quantity = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'this.form.submit();'}), choices=(('0.25', '0.25'), ('0.5', '0.5'), ('0.75', '0.75'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')), label="")