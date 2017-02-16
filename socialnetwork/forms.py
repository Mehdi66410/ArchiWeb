from django import forms

class loginForm(forms.Form):
	username = forms.CharField(label='Pseudo', max_length=100)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class registerForm(forms.Form):
	username = forms.CharField(label='Pseudo', max_length=100)
	email = forms.EmailField(label='Email', max_length=100)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
