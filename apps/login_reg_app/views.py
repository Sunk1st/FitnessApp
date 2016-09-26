from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm, LoginForm
# Create your views here.
def index(request):
    regform = RegisterForm()
    logform = LoginForm()
    context = {
        'registerform' : regform,
        'loginform' : logform
    }
    return render(request, 'login_reg_app/index.html', context)

def register(request):
    fform = RegisterForm()

    if request.methods == 'POST':
        doneform = RegisterForm(request.POST)

        print doneform.is_valid()
        print doneform.errors
        return render(request, 'login_reg_app/index.html', doneform.errors)

def login(request):
    fform = LoginForm()

    if request.methods == 'POST':
        doneform = LoginForm(request.POST)

        print doneform.is_valid()
        print doneform.errors
        return render(request, 'login_reg_app/index.html', doneform.errors)