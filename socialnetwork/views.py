# Importation des bibiliothèques
from django.contrib	import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render

# Importation des modèles
from django.contrib.auth.models import User

# Importation des formulaires
from .forms import loginForm, registerForm


def index(request):
    if request.method == 'POST':
    	form = registerForm(request.POST)
    	user = User.objects.create_user(password=request.POST['password'],email=request.POST['email'],username=request.POST.get('email'))
    	user.save()
    	form = registerForm()
    	return render(request, 'socialnetwork/index.html', {'form': form})
    else :
    	if not request.user.is_authenticated:
    		return render(request,'socialnetwork/index.html')
    	else:
    		return redirect(deconnexion)

def csrf_failure(request, reason=""):
	return  HttpResponseForbidden("Access denied")


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
			user = User.objects.create_user(username=request.POST.get('username'), password=request.POST['password'],email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
			user.save()
			return redirect(connexion)
		else:
			form = registerForm()
		return render(request, 'socialnetwork/registration.html', {'form': form})

#Vérifier si l'utilisateur est connecté
#Exclure l'utilisateur
#Exclure les utilisateurs avec qui il est déjà amis
def listUser(request):
	users  = User.objects.all().exclude(is_staff=True)
	return render(request, 'socialnetwork/listUser.html', {'users': users})

#Vérifier si l'utilisateur est connecté
#Ajouter dans la base si tous les champs sont bon
def addFriend(request):
	if request.method == 'POST':
		form = request.POST
		#if form.is_valid():

	return redirect(listUser)



