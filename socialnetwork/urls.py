from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views

handler404 = 'views.page_not_found'

urlpatterns = [
	url(r'^connexion$', views.connexion, name='connexion'),
	url(r'^mdp_oublie$', views.mdp_oublie, name='mdp_oublie'),
    url(r'^inscription$', views.inscription, name='inscription'),
	url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
	url(r'^editerProfil$', views.editerProfil, name='editerProfil'),
	url(r'^affinite$', views.affinite, name='affinite'),
	url(r'^affinite_suppr$', views.affinite_suppr, name='affinite_suppr'),
	url(r'^chat$', views.chat, name='chat'),
	url(r'^chat_post$', views.chat_post, name='chat_post'),
	url(r'^rencontre$', views.rencontre, name='rencontre'),
	url(r'^discotheque$', views.discotheque, name='discotheque'),
	url(r'^bar$', views.bar, name='bar'),
	url(r'^present$', views.present, name='present'),
	url(r'^presentrestau$', views.presentrestau, name='presentrestau'),
	url(r'^presentdisco$', views.presentdisco, name='presentdisco'),
	url(r'^stars$', views.stars, name='stars'),
	url(r'^starsRestau$', views.starsRestau, name='starsRestau'),
	url(r'^starsDisco$', views.starsDisco, name='starsDisco'),
	url(r'^jaime$', views.jaime, name='jaime'),
	url(r'^jaimepas$', views.jaimepas, name='jaimepas'),
	url(r'^personne_present_bar$', views.personne_present_bar, name='personne_present_bar'),
	url(r'^personne_present_restau$', views.personne_present_restau, name='personne_present_restau'),
	url(r'^personne_present_disco$', views.personne_present_disco, name='personne_present_disco'),
	url(r'^changementloc$', views.changementloc, name='changementloc'),
	url(r'^restaurant$', views.restaurant, name='restaurant'),
	url(r'^menu$', views.menu, name='menu'),
	url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),  # <--
	url(r'^$', views.index, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
