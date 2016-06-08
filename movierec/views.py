from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import LoginForm
from .forms import RegForm
from .forms import RatingsForm
from userfn import addUser, validate, getCurrent
from recommendations import addRating, loadMovies
from recommendations import getRecsUserBased, ratedMovie
import random


def index(request):
	return render(request, "movierec/index.html" )


def register(request):
	if request.method == "POST":
		form= RegForm(request.POST)
		if form.is_valid():
			post = form.save()
			email= form.cleaned_data['email']
			password = form.cleaned_data['password']
			age= form.cleaned_data['age']
			sex= form.cleaned_data['sex']
			occu= form.cleaned_data['occ']
			pin= form.cleaned_data['pin']
			addUser(email,password,age,sex,occu,pin)
			return render(request, 'movierec/newuser.html', {'form': form})
		return render(request, 'movierec/newuser.html', {'form': form})
	else:
		form = RegForm()
	return render(request, 'movierec/register.html', {'form': form})


def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			post=form.save()
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			v=validate(email,password)
			if(v):
				return render(request, 'movierec/newuser.html', {'form': form})
		else:
			return HttpResponse('Invalid', {'form': form})
	else:
		form= LoginForm()
	return render(request, 'movierec/login.html', {'form': form})
 

def newuser (request):
	return render(request, 'movierec/newuser.html')


def rate (request):
	c=getCurrent().rstrip('\n')
	ratings=[]
	moviesfull=loadMovies()
	movies=moviesfull[:]
	#movies=movies[:10]
	random.shuffle(movies)
	movies=movies[:10]
	if request.method=='POST':
		form=RatingsForm(request.POST)
		if form.is_valid():
			for i in range(10):
				mid=0
				rating=form.cleaned_data['rating'+str(i)]
				ratings.append(rating)
				mid=moviesfull.index(movies[i])+1
				addRating(c,mid,ratings[i])
			return render(request, 'movierec/newuser.html')
		else:
			return render(request, 'movierec/rate.html', {'form': form})
	else:
		form=RatingsForm()
	return render(request, 'movierec/rate.html', {'movies': movies})

def rated (request):
	c=getCurrent().rstrip('\n')
	movies=ratedMovie(str(c))
	return render(request, 'movierec/rated.html', {'movies': movies})

def list (request):
	c=getCurrent()
	pred=getRecsUserBased(str(c))
	return render(request, 'movierec/list.html', {'pred':pred})

