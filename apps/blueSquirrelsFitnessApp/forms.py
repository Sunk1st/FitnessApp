from django import forms
from ..login_reg_app.models import User
from django.core.exceptions import ValidationError
import bcrypt

class QuickWeight(forms.ModelForm):
	class Meta:
		model = User
		fields = ('weight',)
	weight = forms.DecimalField(max_digits=5, decimal_places=1)