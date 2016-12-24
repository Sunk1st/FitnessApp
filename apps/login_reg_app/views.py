'''

ValidationError is needed to handle errors from the is_valid call on the class based forms.
messages is needed to be able to view the errors without the page crashing.
bcrypt is used to hash the password.
The forms and models used in this app's view are contained within this app.

'''

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from .models import User
import bcrypt

'''
index displays the login and register forms. This is the first screen a user will arrive at.
Class based forms, RegisterForm and LoginForm, are instantiated and passed into the rendering of the index.html. 
'''

def index(request):
    rform = RegisterForm()
    lform = LoginForm()
    context = {
        'registerform' : rform,
        'loginform' : lform,
    }
    return render(request, 'login_reg_app/index.html', context)

'''
register needs to instantiate the two forms because if the registration process fails, the index page is rendered again. It is rendered again, rather than redirected, because the errors that the is_valid() function gathers are passed into the context as well. It is possible to redirect this by using a keyword argument, but that requires passing the errors in the index function, which is not as related to the errors as the register function is.

Validations are checked via validator methods in models.py as well as a clean method within the RegisterForm class.

The submission will only reach the initial save function if no ValidationError is raised from the clean funtion.

Password is hashed after it is initially saved within the user as it requires far less work. This might be a security issue.

'''

def register(request):
    rform = RegisterForm()
    lform = LoginForm()

    if request.method == 'POST':
        doneform = RegisterForm(request.POST)
        doneform.is_valid()
        try:
            doneform.clean_password2()
            instance = doneform.save(commit=False)
            instance.password = bcrypt.hashpw(instance.password.encode(), bcrypt.gensalt())
            instance.save()
            request.session['user']=request.POST['email']
            return redirect(reverse('fitness_app:index'))
        except ValidationError:
            context = {
                'registerform' : rform,
                'loginform' : lform,
                'errors' : doneform.errors,
            }
            return render(request, 'login_reg_app/index.html', context)

'''

login works very similarly to register. One of the main differences is that checkMatch is called instead of a clean function. At the time, we were unaware of how the naming of clean functions allowed for overriding.

'''

def login(request):
    lform = LoginForm()
    rform = RegisterForm()

    if request.method == 'POST':
        doneform = LoginForm(request.POST)
        doneform.is_valid()
        try:
            doneform.checkMatch() #Should be changed to a clean function
            request.session['user']=request.POST['email']
            return redirect(reverse('fitness_app:index'))
        except ValidationError, err:
            context = {
                'registerform' : rform,
                'loginform' : lform,
                'errors' : err[0]
            }
            return render(request, 'login_reg_app/index.html', context)

'''

Although accessibility to this function only resides within the main app's htmls, it seemed more appropriate to include it here, as it has to do with the rest of the content within this app.

'''

def logout(request):
    request.session.flush()
    return redirect(reverse('login_app:index'))