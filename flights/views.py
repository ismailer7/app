from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Flight
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
	''' is the default page view of our airline application. '''
	if request.user.is_authenticated:
		# if user is already logged in i will display all available flights on home page.
		context = {
			'flights' : Flight.objects.all()
		}
		return render(request, 'flights/index.html', context=context)
	else:
		# else i will display a login page instead of home page
		return render(request, 'flights/login.html')

def flight(request, flight_id):
	''' flight is the view that associated to flight.html page with the flight id passed in the url. '''
	try:
		flight = Flight.objects.get(pk=flight_id)
		# get flight of which the primary key is the flight id, if not exist then raise an exception.
	except Flight.DoesNotExist:
		raise Http404('Flight does not exist.')
	# if everythong went fine then render flight.html with the content of flight and also the passengers
	# associated to that flight.
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

def register(request):
	if request.method == 'POST':
		# means that the user is submitting -> the parameters are going into the body.
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save() # save the user.
			username = form.cleaned_data.get('username') # get the user username
			password = form.cleaned_data.get('password1') # get the user password
			user = authenticate(request,username=username, password=password) #authenticate the user
			login(request, user) # log in
			return HttpResponseRedirect(reverse('index')) # redirect the user to the index page
		else:
			form = UserCreationForm()
			return render(request, 'flights/register.html', {'form' : form})
	else: # GET method
		form = UserCreationForm()
		return render(request, 'flights/register.html', context={ 'form': form })
	