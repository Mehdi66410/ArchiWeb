from django import forms

HOMME = 'H'
FEMME = 'F'
GENRE_CHOICES = (
	(HOMME, 'Homme'),
    (FEMME, 'Femme'),
)

SARTHE = 72
MAYENNE = 53
LOIRE_ATLANTIQUE = 44
MAINE_ET_LOIRE = 49
VENDEE = 85
DEPT_CHOICES = (
	(SARTHE, 'Sarthe'),
	(MAYENNE, 'Mayenne'),
	(MAINE_ET_LOIRE, 'Maine et Loire'),
	(LOIRE_ATLANTIQUE, 'Loire Atlantique'),
	(VENDEE,'Vendee')
)

class loginForm(forms.Form):
	username = forms.CharField(label='Pseudo',min_length=2, max_length=100)
	password = forms.CharField(label='Password',min_length=6, max_length=100, widget=forms.PasswordInput)

class registerForm(forms.Form):
	username = forms.CharField(label='Pseudo', min_length=2, max_length=100)
	email = forms.EmailField(label='Email',min_length=5, max_length=100)
	password = forms.CharField(label='Password',min_length=6, max_length=100, widget=forms.PasswordInput)

class uploadPictureForm(forms.Form):
    picture = forms.FileField()

class updateProfilForm(forms.Form):
	firstname = forms.CharField(label='Prénom', min_length=2, max_length=100, required=False)
	lastname = forms.CharField(label='Nom', min_length=2, max_length=100, required=False)
	username = forms.CharField(label='Pseudo', min_length=2, max_length=100)
	email = forms.EmailField(label='Adresse email',min_length=5, max_length=100)
	password = forms.CharField(label='Mot de passe',min_length=6, max_length=100, widget=forms.PasswordInput, required=False)

class mdpForm(forms.Form):
	username = forms.CharField(label='Pseudo',min_length=2, max_length=100)
	email = forms.EmailField(label='Email',min_length=5, max_length=100)

class informationUserForm(forms.Form):
	genre = forms.ChoiceField(label='Vous êtes ...?', widget=forms.RadioSelect, choices=GENRE_CHOICES, required=True)
	age = forms.IntegerField(label='Age', min_value=18, max_value=100)
	localisation = forms.ChoiceField(label='Localisation', widget=forms.Select, choices=DEPT_CHOICES, required=False)
	profession = forms.CharField(label='Profession', min_length=2, max_length=100, required=False)
	description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'rows': 3}), max_length=250, required=False)

class searchInformationUserForm(forms.Form):
	genre = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENRE_CHOICES, required=True)
	localisation = forms.MultipleChoiceField(label='Localisation', widget=forms.Select, choices=DEPT_CHOICES, required=False)
	ageMin = forms.IntegerField(label='Age minimum', min_value=18, max_value=100)
	ageMax = forms.IntegerField(label='Age maximum', min_value=18, max_value=100)


class sortieForm(forms.Form):
	localisation = forms.MultipleChoiceField(label='Localisation', widget=forms.SelectMultiple, choices=DEPT_CHOICES, required=False)












