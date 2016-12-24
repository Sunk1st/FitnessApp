'''

The class based forms used in this app are all ModelForms. Therefore, we import User from the models.py in this app.

ValidationError allows for the validation of the forms.

'''

from django import forms
from django.core.exceptions import ValidationError
from .models import User
import bcrypt

'''

RegisterForm is tied to the User model by use of the Meta class. The fields that it instantiates are all of the User fields (except for created_at and updated_at)

The measurement fields of User are configured to how the user wants them to be by use of choicefields that display a range of numbers determined by a for loop.

The gender, activity_level, and goal fields are given by hardcoded options, where what they choose is a string, and what is actually saved is either a CharField, DecimalField, or IntegerField.

The two passwords are given the widget passwordInput for good default validation.

password2 is given a label because it is not desirable to display 'Password2' - instead it should be 'Confirm Password'

'''

class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password', 'password2', 'age', 'gender', 'weight', 'feet', 'inches', 'activity_level', 'goal')
	age = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])
	weight = forms.ChoiceField(choices=[(x, x) for x in range(50, 501)])
	feet = forms.ChoiceField(choices=[(x, x) for x in range(1,11)])
	inches = forms.ChoiceField(choices=[(x, x) for x in range(1, 12)])
	gender = forms.ChoiceField(widget=forms.Select, choices=(('Male', 'Male'), ('Female', 'Female')))
	activity_level = forms.ChoiceField(widget=forms.Select, choices=(('1.2', 'Sedentary'), ('1.375', 'Low-Intensity'), ('1.55', 'Medium-Intensity'), ('1.725', 'High-Intensity'), ('1.9', 'Extreme-Intensity')))
	goal = forms.ChoiceField(widget=forms.Select, choices=(('-1000', 'Lose 2 Pounds'), ('-500', 'Lose 1 Pound'), ('0', 'Maintain'), ('500', 'Gain 1 Pound'), ('1000', 'Gain 2 Pounds')))
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)
	password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput, label="Confirm Password")

	'''

	clean_password2 is an overridden function that checks to see if the passwords match. This function is done in this way, rather than included in models.py as an additional default validator, because it needs to access both passwords.

	'''

	def clean_password2(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')

		if not password2:
			raise ValidationError('You must confirm your password')
		if password1 != password2:
			raise ValidationError('Your passwords do not match')
		return password2

'''

LoginForm is not attached to the User model because it does not require this sophistication. It is easily determined to be valid or not within this function.

That being said, checkMatch could be changed to two functions, clean_email and clean_password. This would simplify the code within checkMatch.

'''

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length = 100, widget = forms.PasswordInput)

	'''

	I wonder if it would be better to do the password validation within this function or within views.py.

	'''

	def checkMatch(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		try:
			User.objects.get(email=email)
			user = User.objects.get(email=email)
			password = password.encode()
			userpassword = user.password.encode()
			if bcrypt.hashpw(password, userpassword) != user.password:
				raise ValidationError('Incorrect password!')
		except User.DoesNotExist:
			raise ValidationError('Email not found!')