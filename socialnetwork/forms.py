from django import forms

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

class updateBarLike(forms.Form):
	username = forms.CharField(label='Username', min_length=2, max_length=100)
	barname = forms.CharField(label='BarName', min_length=2, max_length=100)

