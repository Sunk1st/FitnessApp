from django import forms
from .models import User
from django.core.exceptions import ValidationError
import bcrypt


class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password', 'password2', 'age', 'gender', 'weight', 'feet', 'inches', 'activity_level')
	age = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])
	weight = forms.ChoiceField(choices=[(x, x) for x in range(50, 501)])
	feet = forms.ChoiceField(choices=[(x, x) for x in range(1,11)])
	inches = forms.ChoiceField(choices=[(x, x) for x in range(1, 12)])
	gender = forms.ChoiceField(widget=forms.Select, choices=(('Male', 'Male'), ('Female', 'Female')))
	activity_level = forms.ChoiceField(widget=forms.Select, choices=(('1', 'Sedentary'), ('2', 'Low'), ('3', 'Medium'), ('4', 'High')))
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)
	password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput, label="Confirm Password")

	def clean_password2(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise ValidationError('You must confirm your password')
		if password1 != password2:
			raise ValidationError('Your passwords do not match')
		return password2

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)

	def checkMatch(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		print User.objects.get(email=email).password
		if not User.objects.get(email=email):
			raise ValidationError('Email not found!')
		user = User.objects.get(email=email)
		password = password.encode()
		userpassword = user.password.encode()
		if not bcrypt.hashpw(password, userpassword):
			raise ValidationError('Incorrect password!')