from django import forms

class loginForm(forms.Form):
	username = forms.CharField(label='Pseudo', max_length=100)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class registerForm(forms.Form):
	username = forms.CharField(label='Pseudo', max_length=100)
	email = forms.EmailField(label='Email', max_length=100)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class uploadPictureForm(forms.Form):
    picture = forms.FileField()

class updateProfilForm(forms.Form):
	firstname = forms.CharField(label='Prénom', max_length=100)
	lastname = forms.CharField(label='Nom', max_length=100)
	username = forms.CharField(label='Pseudo', max_length=100)
	email = forms.EmailField(label='Adresse email', max_length=100)
	password = forms.CharField(label='Mot de passe', max_length=100, widget=forms.PasswordInput)
	passwordConfirm = forms.CharField(label='Confirmation', max_length=100, widget=forms.PasswordInput)

