# Importation des bibiliothèques
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Importation des modèles
from django.contrib.auth.models import User

# Importation des formulaires
from .forms import loginForm, registerForm


def index(request):
	if not request.user.is_authenticated:
		return redirect(connexion)
	else:
		return HttpResponse('Bienvenue')

def connexion(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'],
			password=request.POST['password'])
		if user is not None:
			login(request, user)
			return redirect(index)
		else:
			return HttpResponse('Erreur de login ou de mot de passe')
	else:
		form = loginForm()
	return render(request, 'socialnetwork/login.html', {'form': form})

def inscription(request):
	if request.method == 'POST':
		form = registerForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
				email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
			user.save()
			return redirect(connexion)
	else:
		form = registerForm()
	return render(request, 'socialnetwork/registration.html', {'form': form})
