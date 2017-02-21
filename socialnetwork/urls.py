from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from . import views

handler404 = 'views.page_not_found'

urlpatterns = [
	url(r'^index/connexion$', views.connexion, name='connexion'),
    url(r'^index/inscription$', views.inscription, name='inscription'),
	url(r'^index/deconnexion$', views.deconnexion, name='deconnexion'),
	url(r'^index/editerProfil$', views.editerProfil, name='editerProfil'),
	url(r'^index/rencontre$', views.rencontre, name='rencontre'),
	url(r'^index/sortie$', views.sortie, name='sortie'),
	url(r'^index/sortie/montemple$', views.montemple, name='montemple'),
	url(r'^index/forum$', views.forum, name='forum'),
	url(r'^listUser$', views.listUser, name='listUser'),
	url(r'^addFriend$', views.addFriend, name='addFriend'),
	url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),  # <--
	url(r'^index/$', views.index, name='index'),
	url(r'^menu/',views.menu,name='menu')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
