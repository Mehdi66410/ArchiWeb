# Importation des bibiliothèques
from django.contrib	import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings

import json
import os
import random

# Importation des modèles
from django.contrib.auth.models import User
from django.db.models import Count, F,FloatField, Sum, Q
from django.contrib.auth.decorators import login_required
from .models import Affinite, Bar, Chat, Discotheque, InformationUser, PictureUser, presentBar, presentDisco, presentRestau, Restaurant, SearchInformationUser, starBar, starDiscotheque, starRestaurant
from django.views.decorators.csrf import csrf_exempt

# Importation des formulaires
from .forms import informationUserForm, loginForm, mdpForm, updateProfilForm, uploadPictureForm, registerForm, searchInformationUserForm, sortieForm

#variable globale
localisation_=72
actual_user_renc = None

# Vue gérant le chargement des affinités
# recupere l'ensemble des affinités où l'utilisateur est l'ajouteur ou l'ajouté et où les confirmations sont à true
@login_required
def affinite(request):
	utilisateur = User.objects.get(pk=request.user.id)
	affinite = Affinite.objects.filter(Q(ajouteur=utilisateur, ajouteurConfirm=True, ajouteConfirm=True) | Q(ajoute=utilisateur, ajouteurConfirm=True, ajouteConfirm=True))
	userInformation = InformationUser.objects.all()
	userPicture = PictureUser.objects.all()
	try:
		# Vérification que le nombre d'affinité est supérieur à 0
		affinite[0]
	except IndexError:
		# Si aucune affinité
		messages.add_message(request, messages.ERROR, "Vous ne possédez aucune affinité")
		messages.add_message(request, messages.WARNING, "N'hésitez pas à aller dans la partie rencontre pour liker des profils")
	return render(request, 'socialnetwork/affinite.html', {'affinite': affinite, 'userInformation': userInformation,'userPicture':userPicture})

# Vue gérant la suppresion d'une affinité
# redirection vers affinite
# recupere l'id de l'affinite et met à false les champs de confirmation de l'objet pour enlever l'affinité
@csrf_exempt
@login_required
def affinite_suppr(request):
	if "suppr" in request.POST:
		affinite_modif = Affinite.objects.get(pk=request.POST['id_affinite'])
		affinite_modif.ajouteurConfirm = False
		affinite_modif.ajouteConfirm = False
		affinite_modif.save()
		messages.add_message(request, messages.WARNING, "Affinité supprimée..")
	return redirect(affinite)

#Fonction qui renvoit la liste des bar pour une certaine localisation
@login_required
def bar(request):
	Bars = Bar.objects.filter(localisation=localisation_)
	present = presentBar.objects.all()
	userPresent=presentBar.objects.filter(id_person=request.user.id)
	sortieForme = sortieForm(request.POST)
	return render(request, 'socialnetwork/bar.html',{'Bars': Bars,'sortieForme': sortieForme, 'present': present,'userPresent':userPresent})

#Fonction qui modifie la localisation et qui renvoit sur la page précédente
@csrf_exempt
def changementloc(request):
	if request.method == 'POST':
		global localisation_
		localisation_ = request.POST['localisation']
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Vue gérant le chargement des informations utiles au chat
# Si non recuperation via formulaire redirection vers affinite
# recupere l'ensemble des messages répondant aux critères et envoie des informations
@login_required
def chat(request):
	if "chat_open" in request.POST or "refresh" in request.POST:
		affinite_chat=Affinite.objects.get(pk=request.POST['id_affinite'])
		chat_message = Chat.objects.filter(Q(emetteur=affinite_chat.ajouteur, recepteur=affinite_chat.ajoute) | Q(emetteur=affinite_chat.ajoute,recepteur=affinite_chat.ajouteur)).order_by('pk')
		utilisateur = User.objects.get(pk=request.user.id)
		affiniteInformation = User.objects.get(pk=affinite_chat.ajouteur.id)
		if affiniteInformation == utilisateur:
			affiniteInformation = User.objects.get(pk=affinite_chat.ajoute.id)
		return render(request, "socialnetwork/chat.html", {'affinite_chat':affinite_chat,'chat_message': chat_message,'affiniteInformation': affiniteInformation})
	return redirect(affinite)

# Vue gérant l'envoi des messages dans le chat et leur enregistrement
# Si non recuperation via formulaire redirection vers affinite
# recupere le message saisi dans le champ input et creer un nouvel element chat
@login_required
def chat_post(request):
	if request.POST:
		msg = request.POST['chat-msg']
		affinite_chat=Affinite.objects.get(pk=request.POST['id_affinite'])
		chat_message = Chat.objects.filter(Q(emetteur=affinite_chat.ajouteur, recepteur=affinite_chat.ajoute) | Q(emetteur=affinite_chat.ajoute,recepteur=affinite_chat.ajouteur)).order_by('pk')
		utilisateur = User.objects.get(pk=request.user.id)
		affiniteInformation = User.objects.get(pk=affinite_chat.ajouteur.id)
		if affiniteInformation == utilisateur:
			affiniteInformation = User.objects.get(pk=affinite_chat.ajoute.id)
		if msg != '':
			c = Chat(emetteur=utilisateur,recepteur=affiniteInformation, message=msg)
			c.save()
		return render(request, "socialnetwork/chat.html",{'affinite_chat':affinite_chat,'chat_message': chat_message,'affiniteInformation': affiniteInformation})
	return redirect(affinite)

# Vue gérant la connexion de l'utilisateur avec le formulaire manuel
# Si authentification correct redirection vers le site
# Sinon affichage d'un message d'erreur + redirection vers l'index
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

# Si echec du csrf
def csrf_failure(request, reason=""):
	return  HttpResponseForbidden("Access denied")

# Vue gérant la déconnexion de l'utilisateur
# Si déconnexion, redirection vers index + message de confirmation
# Sinon, redirection vers connexion si l'utilisateur n'est pas connecté sinon vers le menu du site
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

#Fonction renvoyant la liste des discothèques en fonction de la localisation
@login_required
def discotheque(request):
	Discotheques = Discotheque.objects.filter(localisation=localisation_)
	present = presentDisco.objects.all()
	userPresent=presentDisco.objects.filter(id_person=request.user.id)
	sortieForme = sortieForm(request.POST)
	return render(request, 'socialnetwork/discotheque.html',{'Discotheques': Discotheques,'sortieForme': sortieForme, 'present': present,'userPresent':userPresent})

# Vue gérant l'édition des informations (Nom, Prenom, Mail, Mot de passe, Pseudo) de l'utilisateur et sa photo de profil
def editerProfil(request):
	if request.method == 'POST':
		# Si la vue recoit une demande de modificaiton de la photo de profil
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
				messages.add_message(request, messages.SUCCESS, "Votre photo de profil est bien sauvegardée!")
		else:
			formUploadPicture = uploadPictureForm()

		# Si la vue recoit une demande de modification des informations du profil
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
			messages.add_message(request, messages.SUCCESS, "Vos informations sont bien sauvegardées!")
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

# Vue gérant l'index en fonction de si oui ou non le user est authentifié
def index(request):
	if not request.user.is_authenticated:
		formRegister = registerForm()
		formLogin = loginForm()
		formMdp=mdpForm()
		return render(request,'socialnetwork/index.html', {'formRegister': formRegister, 'formLogin': formLogin,'formMdp': formMdp})
	else:
		return redirect(deconnexion)

# Vue gérant l'inscription manuelle de l'utilisateur
# Une vérification dans la base sur le pseudo est faite avant l'inscription
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

#Fonction qui met j'aime sur une personne, on vérifie au préalable si l'utilisateur a déjà mis j'aime à cette personne, sinon on met j'aime
# et on renvoit les informations (genre, age, profession, etc..) sur la prochaine personne qu'on va afficher
@csrf_exempt
def jaime(request):
	global actual_user_renc
	utilisateur_co = User.objects.get(pk=request.user.id)
	if(actual_user_renc == None):
		actual_user_renc = User.objects.get(pk=request.POST['id_perso'])
	nb_affinite_user = Affinite.objects.filter(ajouteur=utilisateur_co,ajoute=actual_user_renc,ajouteurConfirm=True,ajouteConfirm=False).count()
	if(nb_affinite_user==0):
		affiniteee = Affinite(ajouteur=utilisateur_co, ajoute=actual_user_renc, ajouteurConfirm=True, ajouteConfirm=False)
		affiniteee.save()

	informationUser = InformationUser.objects.get(user=utilisateur_co)
	genreUser = informationUser.genre
	searchInformationUser = SearchInformationUser.objects.get(user=utilisateur_co)
	listeUserAffinite = []
	
	affinites = Affinite.objects.filter(ajouteur=utilisateur_co).all()
	for affinite in affinites:
		if affinite.ajouteur == utilisateur_co:
			listeUserAffinite.append(affinite.ajoute)
		elif affinite.ajoute == utilisateur_co:
			listeUserAffinite.append(affinite.ajouteur)

	if searchInformationUser.genreF == True and searchInformationUser.genreM == True:
		listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=utilisateur_co).all()
	elif searchInformationUser.genreF == True:
		listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=utilisateur_co).filter(genre='F').all()
	elif searchInformationUser.genreM == True:
		listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=utilisateur_co).filter(genre='H').all()
	else:
		listeUserSelect = False
	# On exclue les utilisateurs ayant déja eu une affinité avec
	if len(listeUserAffinite) > 0:

		for affinite in listeUserAffinite:
			listeUserSelect = listeUserSelect.exclude(user=affinite)

		# On récupère la première affinité renvoyée
		userSelect = listeUserSelect.first()
		if(userSelect!=None):
			actual_user_renc = User.objects.get(pk=userSelect.user.id)
		else :
			actual_user_renc=None
	else:
		userSelect = False
	if(userSelect!=None):
		genre_ = userSelect.genre
		local_ = userSelect.localisation
		try:
			userPicture = PictureUser.objects.get(user=userSelect.user.id)
			photo = userPicture.picture
			photo = "/media/" + str(photo)
		except PictureUser.DoesNotExist:
			userPicture = False
			photo = "/media/upload/profilePictureOriginal.jpg"
		if(genre_=="F"):
			genre_="Femme"
		else:
			genre_="Homme"
		if(local_==72):
			local_="Sarthe"
		elif(local_==53):
			local_="Mayenne"
		elif(local_==49):
			local_="Maine et Loire"
		elif(local_==85):
			local_="Vendée"
		else :
			local_="Loire Atlantique"

		information_new = {'nom' : str(userSelect.user),'genre' : genre_, 'age' : str(userSelect.age) + " ans", 'loc' : local_ , 'pro' : str(userSelect.profession), 'pic':photo,'des':str(userSelect.description)} 
		return HttpResponse(json.dumps(information_new))
	return HttpResponse("Aucun profil n'a été trouvé, n'hésitez pas a réessayer plus tard.")

#Fonction qui met j'aime sur une personne, on vérifie au préalable si l'utilisateur a déjà mis j'aime pas à cette personne, sinon on met j'aime
# pas et on renvoit les informations (genre, age, profession, etc..) sur la prochaine personne qu'on va afficher
@csrf_exempt
def jaimepas(request):
	global actual_user_renc
	utilisateur_co = User.objects.get(pk=request.user.id)
	if(actual_user_renc == None):
		actual_user_renc = User.objects.get(pk=request.POST['id_perso'])
	nb_affinite_user = Affinite.objects.filter(ajouteur=utilisateur_co,ajoute=actual_user_renc,ajouteurConfirm=False,ajouteConfirm=False).count()
	if(nb_affinite_user==0):
		affiniteee = Affinite(ajouteur=utilisateur_co, ajoute=actual_user_renc, ajouteurConfirm=False, ajouteConfirm=False)
		affiniteee.save()

	informationUser = InformationUser.objects.get(user=utilisateur_co)
	genreUser = informationUser.genre
	searchInformationUser = SearchInformationUser.objects.get(user=utilisateur_co)
	listeUserAffinite = []
	
	affinites = Affinite.objects.filter(ajouteur=utilisateur_co).all()
	for affinite in affinites:
		if affinite.ajouteur == utilisateur_co:
			listeUserAffinite.append(affinite.ajoute)
		elif affinite.ajoute == utilisateur_co:
			listeUserAffinite.append(affinite.ajouteur)

	if searchInformationUser.genreF == True and searchInformationUser.genreM == True:
		listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=utilisateur_co).all()
	elif searchInformationUser.genreF == True:
		listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=utilisateur_co).filter(genre='F').all()
	elif searchInformationUser.genreM == True:
		listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=utilisateur_co).filter(genre='H').all()
	else:
		listeUserSelect = False
	# On exclue les utilisateurs ayant déja eu une affinité avec
	if len(listeUserAffinite) > 0:

		for affinite in listeUserAffinite:
			listeUserSelect = listeUserSelect.exclude(user=affinite)

		# On récupère la première affinité renvoyée
		userSelect = listeUserSelect.first()
		if(userSelect!=None):
			actual_user_renc = User.objects.get(pk=userSelect.user.id)
		else :
			actual_user_renc=None
	else:
		userSelect = False
	if(userSelect!=None):
		genre_ = userSelect.genre
		local_ = userSelect.localisation
		try:
			userPicture = PictureUser.objects.get(user=userSelect.user.id)
			photo = userPicture.picture
			photo = "/media/" + str(photo)
		except PictureUser.DoesNotExist:
			userPicture = False
			photo = "/media/upload/profilePictureOriginal.jpg"
		if(genre_=="F"):
			genre_="Femme"
		else:
			genre_="Homme"
		if(local_==72):
			local_="Sarthe"
		elif(local_==53):
			local_="Mayenne"
		elif(local_==49):
			local_="Maine et Loire"
		elif(local_==85):
			local_="Vendée"
		else :
			local_="Loire Atlantique"

		information_new = {'nom' : str(userSelect.user),'genre' : genre_, 'age' : str(userSelect.age) + " ans", 'loc' : local_ , 'pro' : str(userSelect.profession), 'pic':photo,'des':str(userSelect.description)} 
		return HttpResponse(json.dumps(information_new))
	return HttpResponse("Aucun profil n'a été trouvé, n'hésitez pas a réessayer plus tard.")

# Vue pour le menu
@login_required
def menu(request):
	form = registerForm(request.POST)
	return render(request, 'socialnetwork/menu.html',{'form': form})

# Vue gérant le mot de passe oublié
# redirection vers index
# Recuperation des valeurs du user pour verifié que les informations sont valides
# Generer d'un nouveau mot de passe et envoie d'un mail à l'adresse du user(terminal)
# Enregistrement nouveau mot de passe
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
			# Generer nouveau mot de passe
			nouveaumotdepasse=''
			for i in range(10):
				nouveaumotdepasse += random.choice("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
			user.set_password(nouveaumotdepasse)
			user.save()
			# Envoie du mail indiquant que le mot de passe à changé
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

# Vue gérant la page 404
def page_not_found(request):
    response = render_to_response('404.html',context_instance=RequestContext(request))
    response.status_code = 404
    return response

# On récupère dans la table presentBar la liste des personnes allant dans le bar où on a cliquer sur "Afficher la liste des personnes présentes"
@csrf_exempt
@login_required
def personne_present_bar(request):
	present = presentBar.objects.values_list('id_person_id',flat=True).filter(id_bar=request.POST['id_bar']) #present[0] contient id première personne qui y va 
	liste = []
	for id_pers in present:
		pers = User.objects.values_list('username',flat=True).filter(pk=id_pers)
		liste.append(pers[0])

	html = ""
	for perso in liste:
		html+=str(perso) + " "
	return HttpResponse(html)

# On récupère dans la table presentDisco la liste des personnes allant dans la discothèque où on a cliquer sur "Afficher la liste des personnes présentes"
@csrf_exempt
@login_required
def personne_present_disco(request):
	present = presentDisco.objects.values_list('id_person_id',flat=True).filter(id_disco=request.POST['id_disco']) #present[0] contient id première personne qui y va 
	liste = []
	for id_pers in present:
		pers = User.objects.values_list('username',flat=True).filter(pk=id_pers)
		liste.append(pers[0])

	html = ""
	for perso in liste:
		html+=str(perso) + " "
	return HttpResponse(html)

# On récupère dans la table presentRestau la liste des personnes allant dans le restaurant où on a cliquer sur "Afficher la liste des personnes présentes"
@csrf_exempt
@login_required
def personne_present_restau(request):
	present = presentRestau.objects.values_list('id_person_id',flat=True).filter(id_restau=request.POST['id_restau']) #present[0] contient id première personne qui y va 
	liste = []
	for id_pers in present:
		pers = User.objects.values_list('username',flat=True).filter(pk=id_pers)
		liste.append(pers[0])

	html = ""
	for perso in liste:
		html+=str(perso) + " "
	return HttpResponse(html)

# Fonction qui permet d'ajouter dans la table presentBar l'utilisateur qui aura choisit d'aller dans un bar
@csrf_exempt
def present(request):
	if request.method == 'POST':
		bar_present = Bar.objects.get(pk=request.POST['id_bar'])
		person_present = User.objects.get(pk=request.user.id)
		present_personne = presentBar(id_person=person_present, id_bar=bar_present)
		present_count_bar_person = presentBar.objects.filter(id_bar=bar_present,id_person=person_present).count()
		if(present_count_bar_person==0):
			present_personne.save()
		else:
			present_personne_ = presentBar.objects.get(id_person=person_present, id_bar=bar_present)
			present_personne_.delete()
		present_count = presentBar.objects.filter(id_bar=bar_present).count()
		return HttpResponse(present_count)

# Fonction qui permet d'ajouter dans la table presentDisco l'utilisateur qui aura choisit d'aller dans une discothèque
@csrf_exempt
def presentdisco(request):
	if request.method == 'POST':
		disco_present = Discotheque.objects.get(pk=request.POST['id_disco'])
		person_present = User.objects.get(pk=request.user.id)
		present_personne = presentDisco(id_person=person_present, id_disco=disco_present)
		present_count_disco_person = presentDisco.objects.filter(id_disco=disco_present,id_person=person_present).count()
		if(present_count_disco_person==0):
			present_personne.save()
		else:
			present_personne_ = presentDisco.objects.get(id_person=person_present, id_disco=disco_present)
			present_personne_.delete()
		present_count = presentDisco.objects.filter(id_disco=disco_present).count()
		return HttpResponse(present_count)

# Fonction qui permet d'ajouter dans la table presentRestau l'utilisateur qui aura choisit d'aller dans un restaurant
@csrf_exempt
def presentrestau(request):
	if request.method == 'POST':
		restau_present = Restaurant.objects.get(pk=request.POST['id_restau'])
		person_present = User.objects.get(pk=request.user.id)
		present_personne = presentRestau(id_person=person_present, id_restau=restau_present)
		present_count_restau_person = presentRestau.objects.filter(id_restau=restau_present,id_person=person_present).count()
		if(present_count_restau_person==0):
			present_personne.save()
		else:
			present_personne_ = presentRestau.objects.get(id_person=person_present, id_restau=restau_present)
			present_personne_.delete()
		present_count = presentRestau.objects.filter(id_restau=restau_present).count()
		return HttpResponse(present_count)

# Vue gérant la page rencontre
@login_required
def rencontre(request):
	swap = True

	utilisateur = User.objects.get(pk=request.user.id)
	if request.method == 'POST':
		# Si l'utilisateur veux modifier ces informations personnelles
		if "informationUser" in request.POST:
			formInformationUser = informationUserForm(request.POST)
			if formInformationUser.is_valid():
				try : 
					informationUser 		= InformationUser.objects.get(user=utilisateur)
					informationUser.genre 		= request.POST['genre']
					informationUser.age 		= request.POST['age']
					informationUser.localisation 	= request.POST['localisation']
					informationUser.profession 	= request.POST['profession']
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

		# Si l'utilisateur veux modifier ces critères de recherche
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

    # On essaye de récupérer les informations de l'utilisateur pour compléter le formulaire
	try:
		informationUser = InformationUser.objects.get(user=utilisateur)
		genreUser = informationUser.genre
		formInformationUser = informationUserForm({'age':informationUser.age, 'localisation': informationUser.localisation, 'profession': informationUser.profession, 'description': informationUser.description})
	except InformationUser.DoesNotExist:
		genreUser = 'H'
		swap = False
		formInformationUser = informationUserForm()

	# On essaye de recupérer les critères de recherche de l'utilisateur pour compléter le formulaires
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
	
	# Si toutes les informations de l'utilisateur sont complétés, on lui propose le swap
	if swap:
		# On récupère la liste des affinités que l'utilisateur a déjà eu
		listeUserAffinite = []
		try :
			affinites = Affinite.objects.filter(Q(ajouteur=utilisateur) | Q(ajoute=utilisateur)).all()
			for affinite in affinites:
				if affinite.ajouteur == utilisateur:
					listeUserAffinite.append(affinite.ajoute)
				elif affinite.ajoute == utilisateur:
					listeUserAffinite.append(affinite.ajouteur)
		except Affinite.DoesNotExist:
			affinites = False
		# On récupère la liste des utilisateurs correspondant aux critères de recherches
		try:
			if searchInformationUser.genreF == True and searchInformationUser.genreM == True:
				listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=request.user.pk).all()
			elif searchInformationUser.genreF == True:
				listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=request.user.pk).filter(genre='F').all()
			elif searchInformationUser.genreM == True:
				listeUserSelect = InformationUser.objects.filter(age__range=(searchInformationUser.ageMin, searchInformationUser.ageMax)).filter(localisation=searchInformationUser.localisation).exclude(user=request.user.pk).filter(genre='H').all()
			else:
				listeUserSelect = False
		except InformationUser.DoesNotExist:
			listeUserSelect = False
		# On exclue les utilisateurs ayant déja eu une affinité avec
		if len(listeUserAffinite) >= 0:
			for affinite in listeUserAffinite:
				listeUserSelect = listeUserSelect.exclude(user=affinite)
			# On récupère la première affinité renvoyée
			try:
				userSelect = listeUserSelect.first()
			except:
				userSelect = False
		else:
			userSelect = False
		# Si un utilisateur a été sélectionné, on récupère ses informations et sa photo
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
		userSelect = False
		userInformation = False
		userPicture = False
		messages.add_message(request, messages.ERROR, "Il est nécéssaire de completer toutes les informations pour pouvoir accéder au swap.")

	# Photo de profil par défault si l'utilisateur n'en a pas ajouté
	if userPicture == False:
		userPicture = PictureUser(picture="/upload/profilePictureOriginal.jpg")

	return render(request, 'socialnetwork/rencontre.html', {'formInformationUser': formInformationUser, 'formSearchInformationUser': formSearchInformationUser, 'genrePerson': genreUser, 'genreSearchM': genreSearchM,'genreSearchF': genreSearchF, 'swap': swap, 'userInformation': userInformation, 'userSelect': userSelect, 'userPicture': userPicture })

#Fonction renvoyant la liste des restaurants en fonction de la localisation
@login_required
def restaurant(request):
	Restaurants = Restaurant.objects.filter(localisation=localisation_)
	present = presentRestau.objects.all()
	userPresent=presentRestau.objects.filter(id_person=request.user.id)
	sortieForme = sortieForm(request.POST)
	return render(request, 'socialnetwork/restaurant.html',{'Restaurants': Restaurants,'sortieForme': sortieForme, 'present': present,'userPresent':userPresent})

# Fonction qui ajoute dans la table starBar la note que l'utilisateur aura mit pour un bar, si il y a déjà une note présente de sa part dans la table, on met la valeur à jour
@csrf_exempt
@login_required
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

# Fonction qui ajoute dans la table starDiscotheque la note que l'utilisateur aura mit pour une discothèque, si il y a déjà une note présente de sa part dans la table, on met la valeur à jour
@csrf_exempt
@login_required
def starsDisco(request):
	valueStar = request.POST['value']
	id_disco = Discotheque.objects.get(pk=request.POST['id_disco'])
	utilisateur = User.objects.get(pk=request.user.id)
	try:
		if request.POST['value']:
			note = starDiscotheque.objects.get(id_user=utilisateur,id_disco=id_disco)
			note.notes=valueStar
			note.save()
	except starDiscotheque.DoesNotExist:
		note = starDiscotheque(id_user=utilisateur, id_disco=id_disco,notes=valueStar)
		note.save()

	nb_disco = float(starDiscotheque.objects.filter(id_disco=id_disco).count())
	s=starDiscotheque.objects.filter(id_disco=id_disco).aggregate(somme_note_disco=Sum('notes'))
	total_note = float(s['somme_note_disco'])
	moy=float(total_note/nb_disco)
	discotheque = Discotheque.objects.get(pk=request.POST['id_disco'])
	discotheque.notes=moy
	discotheque.save()
	return HttpResponse(moy)

# Fonction qui ajoute dans la table starRestaurant la note que l'utilisateur aura mit pour un restaurant, si il y a déjà une note présente de sa part dans la table, on met la valeur à jour
@csrf_exempt
@login_required
def starsRestau(request):
	valueStar = request.POST['value']
	id_resta = Restaurant.objects.get(pk=request.POST['id_restau'])
	utilisateur = User.objects.get(pk=request.user.id)
	try:
		if request.POST['value']:
			note = starRestaurant.objects.get(id_user=utilisateur,id_restau=id_resta)
			note.notes=valueStar
			note.save()
	except starRestaurant.DoesNotExist:
		note = starRestaurant(id_user=utilisateur, id_restau=id_resta,notes=valueStar)
		note.save()

	nb_restau = float(starRestaurant.objects.filter(id_restau=id_resta).count())
	s=starRestaurant.objects.filter(id_restau=id_resta).aggregate(somme_note_restau=Sum('notes'))
	total_note = float(s['somme_note_restau'])
	moy=float(total_note/nb_restau)
	restaurant = Restaurant.objects.get(pk=request.POST['id_restau'])
	restaurant.notes=moy
	restaurant.save()
	return HttpResponse(moy)
