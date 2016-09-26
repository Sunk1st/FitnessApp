from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

def index(request):
	return render(request, 'index.html', name=index)