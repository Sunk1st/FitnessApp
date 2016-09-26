from django import forms
from .models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password', 'password2')
	age = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])
	weight = forms.ChoiceField(choices=[(x, x) for x in range(50, 501)])
	feet = forms.ChoiceField(choices=[(x, x) for x in range(1,11)])
	inches = forms.ChoiceField(choices=[(x, x) for x in range(1, 12)])
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)
	password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise ValidationError("You must confirm your password")
		if password1 != password2:
			raise ValidationError("Your passwords do not match")
		return password2

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)