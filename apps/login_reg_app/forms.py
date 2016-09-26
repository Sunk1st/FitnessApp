from django import forms
from .models import User

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length = 255)
	last_name = forms.CharField(max_length = 255)
	email = forms.EmailField()
	height = forms.IntegerField()
	weight = forms.DecimalField(max_digits=3, decimal_places=2)
	age = forms.DateField()
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)
	confirm_password = forms.CharField(max_length = 100, widget = forms.PasswordInput)

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)