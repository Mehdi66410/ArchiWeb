from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^connexion$', views.connexion, name='connexion'),
    url(r'^inscription$', views.inscription, name='inscription'),
	url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
	url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),  # <--
	url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
]
