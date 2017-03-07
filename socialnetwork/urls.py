from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from . import views

handler404 = 'views.page_not_found'

urlpatterns = [
	url(r'^index/connexion$', views.connexion, name='connexion'),
	url(r'^index/mdp_oublie$', views.mdp_oublie, name='mdp_oublie'),
    url(r'^index/inscription$', views.inscription, name='inscription'),
	url(r'^index/deconnexion$', views.deconnexion, name='deconnexion'),
	url(r'^index/editerProfil$', views.editerProfil, name='editerProfil'),
	url(r'^index/affinite$', views.affinite, name='affinite'),
	url(r'^index/rencontre$', views.rencontre, name='rencontre'),
	url(r'^index/discotheque$', views.discotheque, name='discotheque'),
	url(r'^index/sortie/bar$', views.bar, name='bar'),
	url(r'^index/sortie/ajoutlike$', views.ajoutlike, name='ajoutlike'),
	url(r'^index/sortie/present$', views.present, name='present'),
	url(r'^index/sortie/stars$', views.stars, name='stars'),

	url(r'^index/sortie/changementloc$', views.changementloc, name='changementloc'),
	url(r'^index/sortie/ajoutdislike$', views.ajoutdislike, name='ajoutdislike'),
	url(r'^index/sortie/restaurant$', views.restaurant, name='restaurant'),
	url(r'^index/menu$', views.menu, name='menu'),
	url(r'^listUser$', views.listUser, name='listUser'),
	url(r'^addFriend$', views.addFriend, name='addFriend'),
	url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),  # <--
	url(r'^index/$', views.index, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
