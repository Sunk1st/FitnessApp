from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Food
from .forms import QuickWeight, QuickActivity, QuickGoal, QuantForm
from ..login_reg_app.models import User
from chartit import DataPool, Chart
import unirest
import json
import datetime

'''

index is what displays the home page. This is the function that is called when the user first logs in.

'''

def index(request):
	'''
	The user that is logged in is set to a variable because it is used many times. It is better to store it into a variable rather than have to call the ORM query over and over again. This should save processing speed.
	'''

	user = User.objects.get(email=request.session['user'])

	'''
	Then the basal metabolic rate is determined.
	'''
	if (user.gender == 'Male'):
		bmr = 66.47 + (6.23 * int(user.weight)) + (12.7 * ((user.feet * 12) + user.inches)) - (6.75 * user.age)
	elif (user.gender == 'Female'):
		bmr = 655.1 + (4.35 * int(user.weight)) + (4.7 * (user.feet * 12) + user.inches) - (4.7 * user.age)
	'''
	The daily calories is then determined. Therefore, this is displayed immediately upon login/registration.
	'''
	request.session['dailycal'] = int(float(user.activity_level) * bmr + user.goal)

	'''
	eaten is a queryset that gets all the food the logged in user has eaten today
	'''

	eaten = Food.objects.filter(created_at=datetime.datetime.now().strftime('%Y-%m-%d'), user=user)

	'''
	quantityforms is an array of tuples that have forms and ids. This is necessary to implement a QuantForm for each food. 
	'''

	quantityforms = []
	for food in eaten:
		quantityforms.append((QuantForm(quantity=food.quantity), food.id))

	'''
	the amount of calories and protein already consumed is determined by looping through eaten
	'''

	calsofar = 0
	for food in eaten:
		calsofar += float(food.calories) * float(food.quantity)
	calpercent = (calsofar / request.session['dailycal']) * 100

	protsofar = 0
	for food in eaten:
		protsofar += float(food.protein) * float(food.quantity)
	protpercent = float(protsofar) / (float(user.weight) * 0.6) * 100
	
	context = {
		'user' : user,
		'daily' : request.session['dailycal'],
		'calsofar' : calsofar,
		'calleft' : request.session['dailycal'] - calsofar,
		'calpercent' : calpercent,
		'protsofar' : protsofar,
		'protpercent' : protpercent,
		'protleft' : float(user.weight) * 0.6 - float(protsofar),
		'eaten' : eaten,
		'forms' : quantityforms
	}
	return render(request, 'blueSquirrelsFitnessApp/index.html', context)

def lifestyle(request):
	'''
	The user that is logged in is set to a variable because it is used many times. It is better to store it into a variable rather than have to call the ORM query over and over again. This should save processing speed.
	'''
	user = User.objects.get(email=request.session['user'])

	'''
	
	'''

	qwform = QuickWeight()
	qaform = QuickActivity(level=float(user.activity_level))
	qgform = QuickGoal(goal=user.goal)

	if (user.gender == 'Male'):
		bmr = 66.47 + (6.23 * int(user.weight)) + (12.7 * ((user.feet * 12) + user.inches)) - (6.75 * user.age)
	elif (user.gender == 'Female'):
		bmr = 655.1 + (4.35 * int(user.weight)) + (4.7 * (user.feet * 12) + user.inches) - (4.7 * user.age)

	sedentary = int(bmr * 1.2) + user.goal
	light = int(bmr * 1.375) + user.goal
	moderate = int(bmr * 1.55) + user.goal
	very = int(bmr * 1.725) + user.goal
	extreme = int(bmr * 1.9) + user.goal

	loseTwo = int(bmr * float(user.activity_level)) - 1000
	loseOne = int(bmr * float(user.activity_level)) - 500
	maintain = int(bmr * float(user.activity_level))
	gainOne = int(bmr * float(user.activity_level)) + 500
	gainTwo = int(bmr * float(user.activity_level)) + 1000

	if float(user.activity_level) == 1.200:
		actlvl = 'Sedentary'
	elif float(user.activity_level) == 1.375:
		actlvl = 'Low-Intensity'
	elif float(user.activity_level) == 1.550:
		actlvl = 'Medium-Intensity'
	elif float(user.activity_level) == 1.725:
		actlvl = 'High-Intensity'
	elif float(user.activity_level) == 1.900:
		actlvl = 'Extreme-Intensity'

	if float(user.goal) == -1000:
		gl = 'Lose 2 Pounds'
	elif float(user.goal) == -500:
		gl = 'Lose 1 Pound'
	elif float(user.goal) == 0:
		gl = 'Maintain Weight'
	elif float(user.goal) == 500:
		gl = 'Gain 1 Pound'
	elif float(user.goal) == 1000:
		gl = 'Gain 2 Pounds'

	context = {
		'user' : user,
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
		'gainTwo' : gainTwo,
		'actlvl' : actlvl,
		'gl' : gl
	}

	return render(request, 'blueSquirrelsFitnessApp/lifestyle.html', context)

def analysis(request):

	source = []

	if len(Food.objects.filter()) >= 1:
		source = Food.objects.filter(user=User.objects.get(email=request.session['user']))

	names = []

	for a in Food.objects.filter(user=User.objects.get(email=request.session['user'])):
		names.append(a.food)

	names.reverse()

	caldata = DataPool(
       series=
        [{'options': {
            'source': source},
          'terms': [
            'food',
            'calories'
            ]}])

	calcht = Chart(
        datasource = caldata, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms': {
              'calories': ['calories'],
              }}],
        chart_options = 
          	{'title': {
               'text': 'Calories in ' + ', '.join(names) + ' (from left to right)'},
           	'xAxis' : {
           		'title' : {
           			'text' : ''
           		}
           	}})

	protdata = DataPool(
       series=
        [{'options': {
            'source': source},
          'terms': [
            'food',
            'protein'
            ]}])

	protcht = Chart(
        datasource = protdata, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms': {
              'protein': ['protein'],
              }}],
        chart_options = 
          	{'title': {
               'text': 'Protein in ' + ', '.join(names) + ' (from left to right)'},
           	'xAxis' : {
           		'title' : {
           			'text' : ''
           		}
           	}})

	carbdata = DataPool(
       series=
        [{'options': {
            'source': source},
          'terms': [
            'food',
            'carbohydrates'
            ]}])

	carbcht = Chart(
        datasource = carbdata, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms': {
              'carbohydrates': ['carbohydrates'],
              }}],
        chart_options = 
          	{'title': {
               'text': 'Carbohydrates in ' + ', '.join(names) + ' (from left to right)'},
           	'xAxis' : {
           		'title' : {
           			'text' : ''
           		}
           	}})

	lipdata = DataPool(
       series=
        [{'options': {
            'source': source},
          'terms': [
            'food',
            'lipids'
            ]}])

	lipcht = Chart(
        datasource = lipdata, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms': {
              'lipids': ['lipids'],
              }}],
        chart_options = 
          	{'title': {
               'text': 'Lipids in ' + ', '.join(names) + ' (from left to right)'},
           	'xAxis' : {
           		'title' : {
           			'text' : ''
           		}
           	}})

	context = {
		'user' : User.objects.get(email=request.session['user']),
		'charts' : [calcht, protcht, carbcht, lipcht]
	}
	return render(request, 'blueSquirrelsFitnessApp/analysis.html', context)

def community(request):
	context = {
		'user' : User.objects.get(email=request.session['user']),
		'foods' : Food.objects.all()
	}
	return render(request, 'blueSquirrelsFitnessApp/community.html', context)

def addfood(request):
	name = request.POST['add']
	name = name[4:len(name)]
	response = unirest.get("https://nutritionix-api.p.mashape.com/v1_1/search/" + name + "?fields=item_name%2Cnf_calories%2Cnf_total_fat%2Cnf_protein%2Cnf_trans_fatty_acid%2Cnf_sugars%2Cnf_servings_per_container%2Cnf_total_carbohydrate", headers={"X-Mashape-Key" : "5P8MDOP5irmshHGpT0xH3s2UktVXp1zv2JEjsnpTCinqE6xXj2",
		"Accept" : "application/json"})
	fields = response.body['hits'][0]['fields']

	carbs = fields['nf_total_carbohydrate']
	prot = fields['nf_protein']
	fats = fields['nf_total_fat']
	sugar = fields['nf_sugars']
	if not sugar:
		sugar = 0
	if not carbs:
		carbs = 0
	if not prot:
		prot = 0
	if not fats:
		fats = 0

	Food.objects.create(food=fields['item_name'], calories=fields['nf_calories'], carbohydrates=carbs, lipids=fats, protein=prot, sugar=sugar, user=User.objects.get(email=request.session['user']))
	return redirect(reverse('fitness_app:index'))

def quickweight(request):
	instance = User.objects.get(email=request.session['user'])
	form = QuickWeight(request.POST, instance=instance)
	form.is_valid()
	form.save()
	return redirect(reverse('fitness_app:lifestyle'))

def quickactivity(request):
	instance = User.objects.get(email=request.session['user'])
	form = QuickActivity(request.POST, instance=instance, level=instance.activity_level)
	form.is_valid()
	form.save()
	return redirect(reverse('fitness_app:lifestyle'))

def quickgoal(request):
	instance = User.objects.get(email=request.session['user'])
	form = QuickGoal(request.POST, instance=instance, goal=instance.goal)
	form.is_valid()
	form.save()
	return redirect(reverse('fitness_app:lifestyle'))

def changequant(request, id):
	instance = Food.objects.get(id=id)
	form = QuantForm(request.POST, instance=instance, quantity=instance.quantity)
	form.is_valid()
	form.save()
	return redirect(reverse('fitness_app:index'))

def removefood(request, id):
	Food.objects.get(id=id).delete()
	return redirect(reverse('fitness_app:index'))

def removefoodcomm(request, id):
	Food.objects.get(id=id).delete()
	return redirect(reverse('fitness_app:community'))