from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from ..login_reg_app.models import User
from .forms import QuickWeight, QuickFood

def index(request):
	context = {
		'user' : User.objects.get(email=request.session['user'])
	}
	return render(request, 'blueSquirrelsFitnessApp/bootstrap/index.html', context)

def lifestyle(request):
	qwform = QuickWeight()
	qform = QuickFood()
	userData = User.objects.get(email=request.session['user'])
	if (int(userData.gender[0]) == 1):
		bmr = 66.47 + (13.75 * int(userData.weight)) + (5 * ((userData.feet * 12) + userData.inches) / 2.54) - (6.75 * userData.age)
	else:
		bmr = 655.1 + (4.35 * int(userData.weight)) + (4.7 * (userData.feet * 12) + userData.inches) - (4.7 * userData.age)

	sedentary = int(bmr * 1.2)
	light = int(bmr * 1.375)
	moderate = int(bmr * 1.55)
	very = int(bmr * 1.725)
	extreme = int(bmr * 1.9)
	
	context = {
		'user' : User.objects.get(email=request.session['user']),
		'quickweight' : qwform,
		'quickfood' : qform,
		'bmr' : bmr,
		'sedentary' : sedentary,
		'light' : light,
		'moderate' : moderate,
		'very' : very,
		'extreme' : extreme
	}
	return render(request, 'blueSquirrelsFitnessApp/bootstrap/lifestyle.html', context)

def analysis(request):
	context = {
		'user' : User.objects.get(email=request.session['user'])
	}
	return render(request, 'blueSquirrelsFitnessApp/bootstrap/analysis.html', context)

def community(request):
	context = {
		'user' : User.objects.get(email=request.session['user']),
		'users' : User.objects.all().exclude(email=request.session['user'])
	}
	return render(request, 'blueSquirrelsFitnessApp/bootstrap/community.html')

def food(request):

	return redirect(reverse('fitness_app:lifestyle'))

def quickweight(request):
	instance = User.objects.get(email=request.session['user'])
	form = QuickWeight(request.POST, instance=instance)
	if form.is_valid():
		form.save()
		return redirect(reverse('fitness_app:index'))
	else:
		context = {
			'errors' : form.errors
		}
		return render(request, 'blueSquirrelsFitnessApp/bootstrap/index.html', context)