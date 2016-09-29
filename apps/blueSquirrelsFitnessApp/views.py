from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from ..login_reg_app.models import User
from .models import Food
from .forms import QuickWeight, QuickActivity, QuickGoal
import unirest
import json
import datetime

def index(request):
	user = User.objects.get(email=request.session['user'])
	if (user.gender == 'Male'):
		bmr = 66.47 + (6.23 * int(user.weight)) + (12.7 * ((user.feet * 12) + user.inches)) - (6.75 * user.age)
	elif (user.gender == 'Female'):
		bmr = 655.1 + (4.35 * int(user.weight)) + (4.7 * (user.feet * 12) + user.inches) - (4.7 * user.age)
	request.session['dailycal'] = int(float(user.activity_level) * bmr + user.goal)

	eaten = Food.objects.filter(created_at=datetime.datetime.now(), user=user)

	calsofar = 0
	for food in eaten:
		calsofar += food.calories
	calpercent = (calsofar / request.session['dailycal']) * 100

	protsofar = 0
	for food in eaten:
		protsofar += food.protein
	protpercent = (protsofar / request.session['dailycal']) * 100
	
	context = {
		'user' : user,
		'daily' : request.session['dailycal'],
		'calpercent' : calpercent,
		'protpercent' : protpercent
	}
	return render(request, 'blueSquirrelsFitnessApp/bootstrap/index.html', context)

def lifestyle(request):
	qwform = QuickWeight()
	qaform = QuickActivity()
	qgform = QuickGoal()
	userData = User.objects.get(email=request.session['user'])

	if (userData.gender == 'Male'):
		bmr = 66.47 + (6.23 * int(userData.weight)) + (12.7 * ((userData.feet * 12) + userData.inches)) - (6.75 * userData.age)
	elif (userData.gender == 'Female'):
		bmr = 655.1 + (4.35 * int(userData.weight)) + (4.7 * (userData.feet * 12) + userData.inches) - (4.7 * userData.age)

	sedentary = int(bmr * float(userData.activity_level))
	light = int(bmr * float(userData.activity_level))
	moderate = int(bmr * float(userData.activity_level))
	very = int(bmr * float(userData.activity_level))
	extreme = int(bmr * float(userData.activity_level))

	if (userData.activity_level == 1.2):
		loseTwo = sedentary - 1000
		loseOne = sedentary - 500
		maintain = sedentary 
		gainOne = sedentary + 500
		gainTwo = sedentary + 1000

	elif (userData.activity_level ==1.375):
		loseTwo = light - 1000
		loseOne = light - 500
		maintain = light
		gainOne = light + 500
		gainTwo = light + 1000

	elif (userData.activity_level == 1.55):
		loseTwo = moderate - 1000
		loseOne = moderate - 500
		maintain = moderate
		gainOne = moderate + 500
		gainTwo = moderate + 1000

	elif (userData.activity_level == 1.725):
		loseTwo = very - 1000
		loseOne = very - 500
		maintain = very
		gainOne = very + 500
		gainTwo = very + 1000

	elif (userData.activity_level == 1.9):
		loseTwo = extreme - 1000
		loseOne = extreme - 500
		maintain = extreme
		gainOne = extreme + 500
		gainTwo = extreme + 1000

	
	context = {
		'user' : User.objects.get(email=request.session['user']),
		'yourfoods' : Food.objects.filter(user=User.objects.get(email=request.session['user'])),
		'quickweight' : qwform,
		'quickactivity' : qaform,
		'quickgoal' : qgform,
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
		'foods' : Food.objects.all()
	}
	return render(request, 'blueSquirrelsFitnessApp/bootstrap/community.html', context)

def food(request):

	return redirect(reverse('fitness_app:lifestyle'))

def quickweight(request):
	instance = User.objects.get(email=request.session['user'])
	form = QuickWeight(request.POST, instance=instance)
	if form.is_valid():
		form.save()
		return redirect(reverse('fitness_app:lifestyle'))
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

def quickactivity(request):
	instance = User.objects.get(email=request.session['user'])
	form = QuickActivity(request.POST, instance=instance)
	if form.is_valid():
		form.save()
		return redirect(reverse('fitness_app:lifestyle'))
	else:
		context = {
			'errors' : form.errors
		}
		return render(request, 'blueSquirrelsFitnessApp/bootstrap/index.html', context)

	return redirect(reverse('fitness_app:lifestyle'))

def quickgoal(request):
	instance = User.objects.get(email=request.session['user'])
	form = QuickActivity(request.POST, instance=instance)
	if form.is_valid():
		form.save()
		return redirect(reverse('fitness_app:lifestyle'))
	else:
		context = {
			'errors' : form.errors
		}
		return render(request, 'blueSquirrelsFitnessApp/bootstrap/index.html', context)

	return redirect(reverse('fitness_app:lifestyle'))