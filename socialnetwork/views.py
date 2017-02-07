# Importation des bibiliothèques
from django.contrib	import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Importation des modèles
from django.contrib.auth.models import User

# Importation des formulaires
from .forms import loginForm, registerForm

def index(request):
	if not request.user.is_authenticated:
		return render(request,'socialnetwork/index.html')
	else:
		return redirect(deconnexion)

def connexion(request):
	if request.method == 'POST':
		form = loginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=request.POST['username'],
				password=request.POST['password'])
			if user is not None:
				login(request, user)
				return redirect(deconnexion)
			else:
				messages.add_message(request, messages.WARNING, "Erreur de mot de passe ou de nom d'utilisateur")
	else:
		form = loginForm()
	return render(request, 'socialnetwork/login.html', {'form': form})

def deconnexion(request):
	if request.method == 'POST':
		logout(request)
		return redirect(index)
	else:
		if not request.user.is_authenticated:
			return redirect(connexion)
		else:
			return render(request, 'socialnetwork/logout.html')

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
