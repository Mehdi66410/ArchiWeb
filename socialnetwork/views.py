# Importation des bibiliothèques
from django.contrib	import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render
# Importation des modèles
from django.contrib.auth.models import User

from django.db.models import Q
from django.db.models import Count, F,FloatField, Sum

from .models import PictureUser
from .models import Bar,LikeBar,DislikeBar,presentBar,starBar
from .models import InformationUser, SearchInformationUser
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail
import os
import random
from django.conf import settings

# Importation des formulaires
from .forms import informationUserForm, searchInformationUserForm, loginForm, registerForm, uploadPictureForm, updateProfilForm, mdpForm,sortieForm

localisation_=72

def index(request):
	if not request.user.is_authenticated:
		formRegister = registerForm()
		formLogin = loginForm()
		formMdp=mdpForm()
		return render(request,'socialnetwork/index.html', {'formRegister': formRegister, 'formLogin': formLogin,'formMdp': formMdp})
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
				messages.add_message(request, messages.ERROR, "Erreur de mot de passe ou de nom d'utilisateur")
				return redirect(index)
	else:
		formLogin = loginForm()
	formRegister = registerForm()
	return render(request, 'socialnetwork/index.html', {'formRegister': formRegister, 'formLogin': formLogin})

def deconnexion(request):
	if request.method == 'POST':
		logout(request)
		messages.success(request, "Vous avez été correctement deconnecté! A bientôt..")
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
			username_u = request.POST['username']
			email_u = request.POST['email']
			try:
				user = User.objects.get(username=username_u, email=email_u)
			except User.DoesNotExist:
				messages.add_message(request, messages.ERROR, "Erreur de nom d'utilisateur ou de l'adresse email")
				return redirect(index)
			nouveaumotdepasse=''
			for i in range(10):
				nouveaumotdepasse += random.choice("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
			user.set_password(nouveaumotdepasse)
			user.save()
			send_mail(
    			'Vis Ton Meeting: changement du mot de passe',
    			'A la suite de votre demande, votre mot de passe a été changé. Utilisez désormais '+ nouveaumotdepasse +' À bientôt sur VTM !',
    			settings.EMAIL_HOST_USER,
    			[email_u], fail_silently=False
			)
		else:
			messages.add_message(request, messages.ERROR, "Erreur de nom d'utilisateur ou de l'adresse email")
			return redirect(index)
	messages.success(request, "Votre nouveau mot de passe vous a correctement été envoyé. Vérifiez votre adresse mail!")
	return redirect(index)

def menu(request):
	form = registerForm(request.POST)
	return render(request, 'socialnetwork/menu.html',{'form': form})

@csrf_exempt
def stars(request):
	valueStar = request.POST['value']
	id_barr = Bar.objects.get(pk=request.POST['id_barr'])
	utilisateur = User.objects.get(pk=request.user.id)
	try:
		if request.POST['value']:
			note = starBar.objects.get(id_user=utilisateur,id_bar=id_barr)
			note.notes=valueStar
			note.save()
	except starBar.DoesNotExist:
		note = starBar(id_user=utilisateur, id_bar=id_barr,notes=valueStar)
		note.save()

	nb_bar = float(starBar.objects.filter(id_bar=id_barr).count())
	s=starBar.objects.filter(id_bar=id_barr).aggregate(somme_note_bar=Sum('notes'))
	total_note = float(s['somme_note_bar'])
	moy=float(total_note/nb_bar)
	bar = Bar.objects.get(pk=request.POST['id_barr'])
	bar.notes=moy
	bar.save()
	return HttpResponse(moy)

def affinite(request):
	return render(request, 'socialnetwork/affinite.html')

def rencontre(request):
	swap = True

	utilisateur = User.objects.get(pk=request.user.id)
	if request.method == 'POST':
		if "informationUser" in request.POST:
			formInformationUser = informationUserForm(request.POST)
			if formInformationUser.is_valid():
				try : 
					informationUser 				= InformationUser.objects.get(user=utilisateur)
					informationUser.genre 			= request.POST['genre']
					informationUser.age 			= request.POST['age']
					informationUser.localisation 	= request.POST['localisation']
					informationUser.profession 		= request.POST['profession']
					informationUser.description 	= request.POST['description']
					informationUser.save()
					messages.add_message(request, messages.SUCCESS, "Vos informations ont bien été enregistrés !")
				except InformationUser.DoesNotExist:
					informationUser = InformationUser(user=utilisateur, genre=request.POST['genre'] , localisation=request.POST['localisation'], profession=request.POST['profession'], description=request.POST['description'], age=request.POST['age'])
					informationUser.save()
					messages.add_message(request, messages.SUCCESS, "Vos informations ont bien été enregistrés !")
			else:
				messages.add_message(request, messages.ERROR, "Tout les champs n'ont pas été complété pour sauvegarder vos informations.")
		else:
			formInformationUser = informationUserForm()

		if "searchInformationUser" in request.POST:
			formSearchInformationUser = searchInformationUserForm(request.POST)
			if formSearchInformationUser.is_valid():
				try :
					searchInformationUser = SearchInformationUser.objects.get(user=utilisateur)
					searchInformationUser.ageMin = request.POST['ageMin']
					searchInformationUser.ageMax = request.POST['ageMax']
					
					if "genreF" in request.POST:
						searchInformationUser.genreF = True
					else:
						searchInformationUser.genreF = False

					if "genreM" in request.POST:
						searchInformationUser.genreM = True
					else:
						searchInformationUser.genreM = False

					if request.POST['localisation']:
						searchInformationUser.localisation = request.POST['localisation']

					searchInformationUser.save()
					messages.add_message(request, messages.SUCCESS, "Vos informations ont bien été enregistrés !")

				except SearchInformationUser.DoesNotExist:
					if "genreF" in request.POST:
						genreSearchF = True
					else:
						genreSearchF = False

					if "genreM" in request.POST:
						genreSearchM = True
					else:
						genreSearchM = False

					searchInformationUser = SearchInformationUser(user=utilisateur, ageMin=request.POST['ageMin'], ageMax=request.POST['ageMax'], localisation=request.POST['localisation'], genreF=genreSearchF, genreM=genreSearchM)
					searchInformationUser.save()
					messages.add_message(request, messages.SUCCESS, "Vos informations ont bien été enregistrés !")
			else:
				messages.add_message(request, messages.ERROR, "Tout les champs n'ont pas été complété pour sauvegarder vos critères de recherche.")
		else:
			formSearchInformationUser = searchInformationUserForm()


	try:
		informationUser = InformationUser.objects.get(user=utilisateur)
		genreUser = informationUser.genre
		formInformationUser = informationUserForm({'age':informationUser.age, 'localisation': informationUser.localisation, 'profession': informationUser.profession, 'description': informationUser.description})
	except InformationUser.DoesNotExist:
		genreUser = 'H'
		swap = False
		formInformationUser = informationUserForm()

	try:
		searchInformationUser = SearchInformationUser.objects.get(user=utilisateur)
		genreSearchF = searchInformationUser.genreF
		genreSearchM = searchInformationUser.genreM
		formSearchInformationUser = searchInformationUserForm({'ageMin': searchInformationUser.ageMin, 'ageMax': searchInformationUser.ageMax, 'localisation': searchInformationUser.localisation})
	except SearchInformationUser.DoesNotExist:
		genreSearchM = False
		genreSearchF = False
		swap = False
		formSearchInformationUser = searchInformationUserForm()
		
	if swap:
		messages.add_message(request, messages.SUCCESS, "SWAP OK")
		try:
			userSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=request.user.pk).first()
		except InformationUser.DoesNotExist:
			userSelect = False

		if userSelect:
			try: 
				userInformation = User.objects.get(pk=userSelect.user.pk)
			except User.DoesNotExist:
				userInformation = False

			try:
				userPicture = PictureUser.objects.get(user=userSelect.user.pk)
			except PictureUser.DoesNotExist:
				userPicture = False
		else:
			userInformation = False
			userPicture = False
		

	else:
		# Il est nécéssaire de compléter toutes les information pour pouvoir accéder au SWAP
		messages.add_message(request, messages.ERROR, "Il est nécéssaire de completer toutes les informations pour pouvoir accéder au swap.")


	return render(request, 'socialnetwork/rencontre.html', {'formInformationUser': formInformationUser, 'formSearchInformationUser': formSearchInformationUser, 'genrePerson': genreUser, 'genreSearchM': genreSearchM,'genreSearchF': genreSearchF, 'swap': swap, 'userInformation': userInformation, 'userSelect': userSelect, 'userPicture': userPicture })


def bar(request):
	Bars = Bar.objects.filter(localisation=localisation_)
	Bar_like = LikeBar.objects.all()
	present = presentBar.objects.all()
	sortieForme = sortieForm(request.POST)
	return render(request, 'socialnetwork/bar.html',{'Bars': Bars, 'Bar_like': Bar_like, 'sortieForme': sortieForme, 'present': present})

@csrf_exempt
def personne_present_bar(request):
	present = presentBar.objects.values_list('id_person_id',flat=True).filter(id_bar=request.POST['id_bar']) #present[0] contient id première personne qui y va 
	liste = []
	for id_pers in present:
		pers = User.objects.values_list('username',flat=True).filter(pk=id_pers)
		liste.append(pers[0])

	html = ""
	for perso in liste:
		html+=str(perso) + " "

	print(html)
	return HttpResponse(html)


@csrf_exempt
def ajoutlike(request):
	if request.method == 'POST':
		bar_like = Bar.objects.get(pk=request.POST['id_like'])
		person_like = User.objects.get(pk=request.user.id)
		like_count_bar_person = LikeBar.objects.filter(bar_name=bar_like,person_name=person_like).count()
		if(like_count_bar_person==0):
			like = LikeBar(person_name=person_like, bar_name=bar_like)
			like.save()
		like_count = LikeBar.objects.filter(bar_name=bar_like).count()
		return HttpResponse(like_count)

@csrf_exempt
def present(request):
	if request.method == 'POST':
		bar_present = Bar.objects.get(pk=request.POST['id_bar'])
		person_present = User.objects.get(pk=request.user.id)
		present_personne = presentBar(id_person=person_present, id_bar=bar_present)
		present_count_bar_person = presentBar.objects.filter(id_bar=bar_present,id_person=person_present).count()
		if(present_count_bar_person==0):
			present_personne.save()
		present_count = presentBar.objects.filter(id_bar=bar_present).count()
		return HttpResponse(present_count)

@csrf_exempt
def ajoutdislike(request):
	if request.method == 'POST':
		bar_dislike = Bar.objects.get(pk=request.POST['id_like'])
		person_dislike = User.objects.get(pk=request.user.id)
		dislike_count_bar_person = DislikeBar.objects.filter(bar_name=bar_dislike,person_name=person_dislike).count()
		if(dislike_count_bar_person==0):
			dislike = DislikeBar(person_name=person_dislike, bar_name=bar_dislike)
			dislike.save()
		dislike_count = DislikeBar.objects.filter(bar_name=bar_dislike).count()
		return HttpResponse(dislike_count)


def restaurant(request):
	return render(request, 'socialnetwork/restaurant.html')

def discotheque(request):
	return render(request, 'socialnetwork/discotheque.html')

@csrf_exempt
def changementloc(request):
	if request.method == 'POST':
		global localisation_
		localisation_ = request.POST['id_localisation']
	return redirect(bar)

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

def inscription(request):
	if request.method == 'POST':
		form = registerForm(request.POST)
		if form.is_valid():
			username_u=request.POST['username']
			try:
				user = User.objects.get(username=username_u)
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST.get('username'), password=request.POST['password'],email=request.POST['email'])
				user.save()
				user = authenticate(username=request.POST['username'], password=request.POST['password'])
				login(request, user)
				messages.success(request, "Vous êtes à présent inscrit, profitez et faites des rencontres!")
				return redirect(deconnexion)
			messages.add_message(request, messages.ERROR, "Erreur ce pseudo correspond déjà à un profil existant!")
			return redirect(index)
		else:
			messages.add_message(request, messages.ERROR, "Erreur formulaire!")
			return redirect(index)
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


