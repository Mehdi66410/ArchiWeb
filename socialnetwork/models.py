from django.db import models

# Importation des modèles
from django.contrib.auth.models import User

# Create your models here.

class Friend(models.Model):
	ajouteur = models.OneToOneField(User, related_name='ajouteur')
	ajoute = models.OneToOneField(User, related_name='ajoute')
	confirme = models.BooleanField(default=False)
	add_date = models.DateField()

class PictureUser(models.Model):
	user = models.ForeignKey(User)
	picture = models.FileField(upload_to='upload')
	add_date = models.DateField()