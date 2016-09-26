from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.core.exceptions import ValidationError
# Create your views here.
def index(request):
    rform = RegisterForm()
    lform = LoginForm()
    context = {
        'registerform' : rform,
        'loginform' : lform
    }
    return render(request, 'login_reg_app/index.html', context)

def register(request):
    rform = RegisterForm()
    lform = LoginForm()

    if request.method == 'POST':
        doneform = RegisterForm(request.POST)
        doneform.is_valid()
        try:
            doneform.clean_password2()
        except ValidationError:
            pass

        context = {
            'registerform' : rform,
            'loginform' : lform,
            'errors' : doneform.errors
        }
        return render(request, 'login_reg_app/index.html', context)

def login(request):
    fform = LoginForm()

    if request.method == 'POST':
        doneform = LoginForm(request.POST)

        return render(request, 'login_reg_app/index.html', doneform.errors)