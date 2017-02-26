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
	add_date = models.DateField(auto_now_add=True)


class Bar(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	picture = models.FileField(upload_to='upload',default='')
	speciality = models.CharField(max_length=100, default='')
	prix = models.IntegerField(default=5)

class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	picture = models.FileField(upload_to='upload',default='')
	speciality = models.CharField(max_length=100, default='')
	prix = models.IntegerField(default=25)