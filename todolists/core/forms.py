from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  password2 = forms.CharField(label='Confirm', help_text='Required', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'email', 'birth_date', 'password1', 'password2',)
  #   labels = {
  #     "password2": "Confirm",
  #   }

class UserLoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=50, help_text='Required.')
	password = forms.CharField(label='Password', help_text='Required', widget=forms.PasswordInput)

  # class Meta:
  #   model = User
  #   fields = ('username', 'password',)
  #   labels = {
  #     "username": "Name",
  #   }
