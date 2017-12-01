from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from profiles.models import Profile, AgeValidator
from list.models import List
from items.models import Item, ITEM_STATUS
from django.contrib.admin import widgets


class UserRegistrationForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
  last_name = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
  username = forms.CharField(min_length=3, max_length=30, required=True, help_text='', label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  birth_date = forms.DateField(help_text='', label='', required=True, validators=[AgeValidator], widget=forms.DateInput(attrs={'class': 'date-input', 'placeholder': 'Birthday', 'type': 'date'}))
  email = forms.EmailField(max_length=254, help_text='', label='', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
  password1 = forms.CharField(max_length=30, help_text='', label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  password2 = forms.CharField(max_length=30, help_text='', label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  bio = forms.CharField(max_length=300, help_text='', required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Bio'}))

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'email', 'birth_date', 'password1', 'password2',)


class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(max_length=30, help_text='', label='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

  # class Meta:
  #   model = User
  #   fields = ('username', 'password',)
  #   labels = {
  #     "username": "Name",
  #   }


class UserUpdateEmailForm(ModelForm):
  email = forms.EmailField(max_length=254, required=True, help_text='', label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

  class Meta:
    model = User
    fields = ('email',)


class UserUpdatePasswordForm(forms.Form):
  current_password = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}))
  password1 = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
  password2 = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

  class Meta:
    model = User
    fields = ('current_password', 'password1', 'password2')


class UserUpdateNameForm(ModelForm):
  first_name = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
  last_name = forms.CharField(max_length=30, help_text='', required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

  class Meta:
    model = User
    fields = ('first_name', 'last_name',)


class UserUpdateBioForm(ModelForm):
  bio = forms.CharField(max_length=300, help_text='', label='', required=False, widget=forms.Textarea(attrs={'placeholder': 'Edit Bio Here'}))

  class Meta:
    model = Profile
    fields= ('bio',)


class KitchenEditForm(ModelForm):
  description = forms.CharField(max_length=300, help_text='', label='', required=False, widget=forms.Textarea(attrs={'placeholder': 'Edit Description Here'}))
  private = forms.BooleanField(required=False, help_text='', label='Check to keep private.', widget=forms.CheckboxInput(attrs={'placeholder': 'Private', 'label': 'Private'}))

  class Meta:
    model = List
    fields = ('description', 'private')


class NewKitchenForm(KitchenEditForm):
  title = forms.CharField(max_length=50, help_text='', label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Title'}))

  class Meta:
    model = List
    fields = ('title', 'description', 'private',)

class ItemForm(ModelForm):
  name = forms.CharField(max_length=30, label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Item'}))
  status = forms.ChoiceField(choices=ITEM_STATUS, label='', widget=forms.Select(attrs={'placeholder': 'Status'}) )
  notes = forms.CharField(max_length=100, help_text='', label='', required=True, widget=forms.Textarea(attrs={'placeholder': 'Notes', }))

  class Meta:
    model = Item
    fields = ('name', 'status', 'notes',)

class ItemEditForm(ModelForm):
  notes = forms.CharField(max_length=100, help_text='', label='', required=True, widget=forms.Textarea(attrs={'placeholder': 'Notes', }))

  class Meta:
    model = Item
    fields = ('notes',)