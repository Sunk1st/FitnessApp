from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from ..login_reg_app.models import User
from .forms import QuickWeight
import unirest
import json

def index(request):
	context = {
		'user' : User.objects.get(email=request.session['user'])
	}
	return render(request, 'blueSquirrelsFitnessApp/bootstrap/index.html', context)

def lifestyle(request):
	qwform = QuickWeight()
	userData = User.objects.get(email=request.session['user'])
	if (userData.gender == 'Male'):
		bmr = 66.47 + (6.23 * int(userData.weight)) + (12.7 * ((userData.feet * 12) + userData.inches)) - (6.75 * userData.age)
	elif (userData.gender == 'Female'):
		bmr = 655.1 + (4.35 * int(userData.weight)) + (4.7 * (userData.feet * 12) + userData.inches) - (4.7 * userData.age)

	sedentary = int(bmr * 1.2)
	light = int(bmr * 1.375)
	moderate = int(bmr * 1.55)
	very = int(bmr * 1.725)
	extreme = int(bmr * 1.9)

	if (userData.activity_level == 1):
		loseTwo = sedentary - 1000
		loseOne = sedentary - 500
		maintain = sedentary 
		gainOne = sedentary + 500
		gainTwo = sedentary + 1000

	elif (userData.activity_level == 2):
		loseTwo = light - 1000
		loseOne = light - 500
		maintain = light
		gainOne = light + 500
		gainTwo = light + 1000

	elif (userData.activity_level == 3):
		loseTwo = moderate - 1000
		loseOne = moderate - 500
		maintain = moderate
		gainOne = moderate + 500
		gainTwo = moderate + 1000

	elif (userData.activity_level == 4):
		loseTwo = very - 1000
		loseOne = very - 500
		maintain = very
		gainOne = very + 500
		gainTwo = very + 1000

	elif (userData.activity_level == 5):
		loseTwo = extreme - 1000
		loseOne = extreme - 500
		maintain = extreme
		gainOne = extreme + 500
		gainTwo = extreme + 1000

	
	context = {
		'user' : User.objects.get(email=request.session['user']),
		'quickweight' : qwform,
		'bmr' : bmr,
		'sedentary' : sedentary,
		'light' : light,
		'moderate' : moderate,
		'very' : very,
		'extreme' : extreme,
		'loseTwo' : loseTwo,
		'loseOne' : loseOne,
		'maintain' : maintain,
		'gainOne' : gainOne,
		'gainTwo' : gainTwo
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

def getfood(request):
	
	print response.body
	print request.POST['test']
	return HttpResponse(json.dumps(response.body))


def addfood(request):
	
	response = unirest.get("https://nutritionix-api.p.mashape.com/v1_1/search/" + request.POST['foodname'] + "?fields=item_name%2Cnf_calories%2Cnf_total_fat%2Cnf_protein%2Cnf_trans_fatty_acid%2Cnf_sugars%2Cnf_servings_per_container%2Cnf_total_carbohydrate", headers={"X-Mashape-Key" : "5P8MDOP5irmshHGpT0xH3s2UktVXp1zv2JEjsnpTCinqE6xXj2",
		"Accept" : "application/json"})
	return redirect(reverse('fitness_app:lifestyle'))