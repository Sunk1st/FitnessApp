from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from ..login_reg_app.models import User
from .models import Food
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
		bmr = 66.47 + (13.75 * int(userData.weight)) + (5 * ((userData.feet * 12) + userData.inches) / 2.54) - (6.75 * userData.age)
	elif userData.gender == 'Female':
		bmr = 655.1 + (4.35 * int(userData.weight)) + (4.7 * (userData.feet * 12) + userData.inches) - (4.7 * userData.age)

	sedentary = int(bmr * 1.2)
	light = int(bmr * 1.375)
	moderate = int(bmr * 1.55)
	very = int(bmr * 1.725)
	extreme = int(bmr * 1.9)
	
	context = {
		'user' : User.objects.get(email=request.session['user']),
		'yourfoods' : Food.objects.filter(user=User.objects.get(email=request.session['user'])),
		'quickweight' : qwform,
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


def addfood(request):
	name = request.POST['add']
	name = name[4:len(name)]
	response = unirest.get("https://nutritionix-api.p.mashape.com/v1_1/search/" + name + "?fields=item_name%2Cnf_calories%2Cnf_total_fat%2Cnf_protein%2Cnf_trans_fatty_acid%2Cnf_sugars%2Cnf_servings_per_container%2Cnf_total_carbohydrate", headers={"X-Mashape-Key" : "5P8MDOP5irmshHGpT0xH3s2UktVXp1zv2JEjsnpTCinqE6xXj2",
		"Accept" : "application/json"})
	fields = response.body['hits'][0]['fields']
	Food.objects.create(food=fields['item_name'], calories=fields['nf_calories'], carbohydrates=fields['nf_total_carbohydrate'], lipids=fields['nf_total_fat'], protein=fields['nf_protein'], sugar=fields['nf_sugars'], user=User.objects.get(email=request.session['user']))
	return redirect(reverse('fitness_app:lifestyle'))