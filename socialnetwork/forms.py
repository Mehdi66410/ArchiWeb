from django import forms

class loginForm(forms.Form):
	username = forms.CharField(label='Pseudo', max_length=100)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class registerForm(forms.Form):
	username = forms.CharField(label='Pseudo', min_length=2, max_length=100)
	email = forms.EmailField(label='Email', max_length=100)
	password = forms.CharField(label='Password', min_length=2, max_length=100, widget=forms.PasswordInput)

class uploadPictureForm(forms.Form):
    picture = forms.FileField()

class updateProfilForm(forms.Form):
	firstname = forms.CharField(label='Prénom', min_length=2, max_length=100, required=False)
	lastname = forms.CharField(label='Nom', min_length=2, max_length=100, required=False)
	username = forms.CharField(label='Pseudo', min_length=2, max_length=100)
	email = forms.EmailField(label='Adresse email', max_length=100)
	password = forms.CharField(label='Mot de passe', min_length=2, max_length=100, widget=forms.PasswordInput, required=False)

class mdpForm(forms.Form):
	username = forms.CharField(label='Pseudo', max_length=100)
	email = forms.EmailField(label='Email', max_length=100)
