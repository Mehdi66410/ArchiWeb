from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^connexion$', views.connexion, name='connexion'),
	url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
	url(r'^inscription$', views.inscription, name='inscription'),
    url(r'^accueil$',views.accueil,name='accueil'),
    url(r'^$', views.index, name='index'),
]
