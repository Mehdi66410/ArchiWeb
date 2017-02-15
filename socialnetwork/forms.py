from django import forms

class loginForm(forms.Form):
	email = forms.CharField(label='email', max_length=100)
	username = email
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class registerForm(forms.Form):
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
	email = forms.EmailField(label='Email', max_length=100)
	username = email
