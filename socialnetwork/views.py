# Importation des bibiliothèques
from django.contrib	import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render
# Importation des modèles
from django.contrib.auth.models import User
from .models import PictureUser
from .models import Bar

import os
from django.conf import settings

# Importation des formulaires
from .forms import loginForm, registerForm, uploadPictureForm, updateProfilForm

def index(request):
	if not request.user.is_authenticated:
		formRegister = registerForm()
		formLogin = loginForm()
		return render(request,'socialnetwork/index.html', {'formRegister': formRegister, 'formLogin': formLogin})
	else:
		return redirect(deconnexion)

def csrf_failure(request, reason=""):
	return  HttpResponseForbidden("Access denied")

def page_not_found(request):
    response = render_to_response('404.html',context_instance=RequestContext(request))
    response.status_code = 404

    return response

def connexion(request):
	if request.method == 'POST':
		formLogin = loginForm(request.POST)
		if formLogin.is_valid():
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			if user is not None:
				login(request, user)
				return redirect(deconnexion)
			else:
				messages.add_message(request, messages.WARNING, "Erreur de mot de passe ou de nom d'utilisateur")
	else:
		formLogin = loginForm()
	formRegister = registerForm()
	return render(request, 'socialnetwork/index.html', {'formRegister': formRegister, 'formLogin': formLogin})

def deconnexion(request):
	if request.method == 'POST':
		logout(request)
		return redirect(index)
	else:
		if not request.user.is_authenticated:
			return redirect(connexion)
		else:
			return render(request, 'socialnetwork/menu.html')

def mdp_oublie(request):
	if request.method == 'POST':
		formMdp = mdpForm(request.POST)
		if formMdp.is_valid():
			user=User.objects.get(username=request.POST['username'])
			courriel=User.objects.get(email=request.POST['email'])
			nouveaumotdepasse=''
			for i in range(10):
				nouveaumotdepasse += random.choice("abcdefghijklmnopqrstuvwxyz0123456789éàèù@µ_-")
			user.set_password(nouveaumotdepasse)
			user.save()
			send_mail(
    			user+', changement du mot de passe',
    			'Votre mot de passe a été changé c est désormais '+ nouveaumotdepasse +' À bientôt !',
    			'from@VTM.com',
    			[courriel],
    			fail_silently=False,
			)

def affinite(request):
	return render(request, 'socialnetwork/affinite.html')

def rencontre(request):
	return render(request, 'socialnetwork/rencontre.html')

def montemple(request):
	return render(request, 'socialnetwork/montemple.html')

def bar(request):
	Bars = Bar.objects.all()
	return render(request, 'socialnetwork/bar.html',{'Bars': Bars})

def restaurant(request):
	return render(request, 'socialnetwork/restaurant.html')

def sortie(request):
	return render(request, 'socialnetwork/sortie.html')

def forum(request):
	return render(request, 'socialnetwork/forum.html')

def editerProfil(request):
	if request.method == 'POST':
		if "uploadPicture" in request.POST:
			formUploadPicture = uploadPictureForm(request.POST,request.FILES)
			if formUploadPicture.is_valid():
				
				try : 
					picture = PictureUser.objects.get(user=User.objects.get(pk=request.user.id))
					picture.picture.delete()
					picture.picture=request.FILES['picture']
					picture.save()
				except PictureUser.DoesNotExist:
					picture = PictureUser(user=User.objects.get(pk=request.user.id), picture=request.FILES['picture'])
					picture.save()
		else:
			formUploadPicture = uploadPictureForm()

		if "modifInfo" in request.POST:
			formUpdateProfil = updateProfilForm(request.POST)
			user = User.objects.get(pk=request.user.id)
				
			if request.POST['firstname']:
				user.first_name = request.POST['firstname']
				
			if request.POST['lastname']:
				user.last_name = request.POST['lastname']
				
			if request.POST['password']:
				user.set_password(request.POST['password'])

			user.email = request.POST['email']
			user.pseudo = request.POST['username']
			user.save()
		else:
			formUpdateProfil = updateProfilForm({'firstname': request.user.first_name, 'lastname': request.user.last_name, 'username': request.user.username, 'email': request.user.email})
	
	else:
		formUploadPicture = uploadPictureForm()
		formUpdateProfil = updateProfilForm({'firstname': request.user.first_name, 'lastname': request.user.last_name, 'username': request.user.username, 'email': request.user.email})
	
	try:
		lienPicture = PictureUser.objects.get(user=User.objects.get(pk=request.user.id))
	except PictureUser.DoesNotExist:
		lienPicture = PictureUser(picture="/upload/profilePictureOriginal.jpg")

	return render(request, 'socialnetwork/editerProfil.html', {'formUploadPicture': formUploadPicture, 'formEditProfil': formUpdateProfil, 'lienPicture': lienPicture.picture})

def menu(request):
	return render(request, 'socialnetwork/menu.html', {'form': form})

def inscription(request):
	if request.method == 'POST':
		form = registerForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=request.POST.get('username'), password=request.POST['password'],email=request.POST['email'])
			user.save()
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)
			return redirect(deconnexion)
	else:
		form = registerForm()
	return render(request, 'socialnetwork/index.html', {'form': form})

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


