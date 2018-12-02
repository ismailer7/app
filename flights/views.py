from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Flight

# Create your views here.

def index(request):
	if request.user.is_authenticated:
		context = {
			'flights' : Flight.objects.all()
		}
		return render(request, 'flights/index.html', context=context)
	else:
		return render(request, 'flights/login.html')

def flight(request, flight_id):
	try:
		flight = Flight.objects.get(pk=flight_id)
	except Flight.DoesNotExist:
		raise Http404('Flight does not exist.')

	context = {
		'flight' : flight,
		'passengers' : flight.passengers.all()
	}
	return render(request, 'flights/flight.html', context=context)

def login_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request, 'flights/login.html', {'message' : 'Invalid sername or/and passwrod'})
	return render(request, 'flights/login.html')

def login_out(request):
	logout(request)
	return render(request, 'flights/login.html', {'message' : 'You Logged Out'})