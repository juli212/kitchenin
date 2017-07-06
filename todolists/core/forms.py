from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'birth_date', 'email', 'password1', 'password2',)
      labels = {
        'password2': 'Confirm',
      }

class UserLoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=50, help_text='Required.')
	password = forms.CharField(label='Password', help_text='Required', widget=forms.PasswordInput)

	# class Meta:
	# 	model = User
	# 	fields = ('username', 'password',)