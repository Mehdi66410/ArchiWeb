from django.db import models

# Importation des modeles
from django.contrib.auth.models import User

# Constant Models

HOMME = 'H'
FEMME = 'F'
GENRE_CHOICES = (
	(HOMME, 'Homme'),
    (FEMME, 'Femme'),
)

SARTHE = 72
MAYENNE = 53
DEPT_CHOICES = (
	(SARTHE, 'Sarthe'),
	(MAYENNE, 'Mayenne')
)

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
	localisation = models.IntegerField(choices=DEPT_CHOICES,default=72)
	picture = models.FileField(upload_to='upload',default='')
	speciality = models.CharField(max_length=100, default='')
	prix = models.IntegerField(default=5)
	description = models.CharField(max_length=10000,default='')

class Restaurant(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	localisation = models.IntegerField(choices=DEPT_CHOICES,default=72)
	picture = models.FileField(upload_to='upload',default='')
	speciality = models.CharField(max_length=100, default='')
	prix = models.IntegerField(default=25)
	description = models.CharField(max_length=10000,default='')

class jaimeBar(models.Model):
	name = models.ForeignKey(Bar)
	personne = models.ForeignKey(User)

class presentBar(models.Model):
	name = models.ForeignKey(Bar)
	personne = models.ForeignKey(User)

class informationUser(models.Model):
	user = models.ForeignKey(User)
	localisation = models.IntegerField(choices=DEPT_CHOICES)
	age = models.IntegerField()
	description = models.CharField(max_length=500)

class searchInformationUser(models.Model):
	user = models.ForeignKey(User)
	localisation = models.IntegerField(choices=DEPT_CHOICES)
	ageMin = models.IntegerField()
	ageMax = models.IntegerField()