from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from profiles.models import Profile, AgeValidator
from list.models import List
from items.models import Item, ITEM_STATUS
from django.contrib.admin import widgets
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


d = date.today() - relativedelta(years=18)
# basic = [help_text='', label_suffix='']


class UserRegistrationForm(UserCreationForm):
  first_name = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='First Name',
    label_suffix="",
    # basic,
    widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
  last_name = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='Last Name',
    label_suffix="",
    widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
  username = forms.CharField(
    min_length=3,
    max_length=30,
    required=True,
    help_text='',
    label_suffix="",
    widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  birth_date = forms.DateField(
    help_text='',
    label='Birthday',
    required=True,
    validators=[AgeValidator],
    label_suffix="",
    widget=forms.DateInput(attrs={'class': 'date-input', 'placeholder': 'Birthday', 'type': 'date', 'value': d, 'max': d}))
  email = forms.EmailField(
    max_length=254,
    help_text='',
    label='Email',
    required=True,
    label_suffix="",
    widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
  password1 = forms.CharField(
    max_length=30,
    help_text='',
    label='Password',
    required=True,
    label_suffix="",
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  password2 = forms.CharField(
    max_length=30,
    help_text='',
    label='Confirm Password',
    required=True,
    label_suffix="",
    widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  bio = forms.CharField(
    max_length=300,
    help_text='',
    required=False,
    label='Bio',
    label_suffix="",
    widget=forms.Textarea(attrs={'placeholder': 'Bio'}))

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'email', 'birth_date', 'password1', 'password2',)


class UserLoginForm(forms.Form):
  username = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='Username',
    label_suffix="",
    error_messages=({'invalid': 'Invalid Username'}),
    widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  password = forms.CharField(
    max_length=30,
    help_text='',
    label='Password',
    required=True,
    label_suffix="",
    error_messages={'invalid': 'Invalid Password'},
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

  def clean(self):
    data = self.cleaned_data
    user = authenticate(username=data['username'], password=data['password'])
    if not User.objects.filter(username=data['username']):
      raise ValidationError('User does not exist')
    elif user is None:
      raise ValidationError('User or password are incorrect')
    return data

  class Meta:
    model = User
    fields = ('username', 'password')



class UserUpdateEmailForm(ModelForm):
  email = forms.EmailField(
    max_length=254,
    required=True,
    help_text='',
    label='Email',
    label_suffix="",
    widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

  class Meta:
    model = User
    fields = ('email',)


class UserUpdatePasswordForm(forms.Form):
  current_password = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='Current Password',
    label_suffix="",
    widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}))
  password1 = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='New Password',
    label_suffix="",
    widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
  password2 = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='Confirm New Password',
    label_suffix="",
    widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

  class Meta:
    model = User
    fields = ('current_password', 'password1', 'password2')


class UserUpdateNameForm(ModelForm):
  first_name = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='First Name',
    label_suffix="",
    widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
  last_name = forms.CharField(
    max_length=30,
    help_text='',
    required=True,
    label='Last Name',
    label_suffix="",
    widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

  class Meta:
    model = User
    fields = ('first_name', 'last_name',)


class UserUpdateBioForm(ModelForm):
  bio = forms.CharField(
    max_length=300,
    help_text='',
    label='Bio',
    required=False,
    label_suffix="",
    widget=forms.Textarea(attrs={'placeholder': 'Edit Bio Here'}))

  class Meta:
    model = Profile
    fields= ('bio',)


class KitchenEditForm(ModelForm):
  description = forms.CharField(
    max_length=300,
    help_text='',
    label='Description',
    required=False,
    label_suffix="",
    widget=forms.Textarea(attrs={'placeholder': 'Edit Description Here'}))
  private = forms.BooleanField(
    required=False,
    help_text='',
    label='Check to keep private.',
    label_suffix="",
    widget=forms.CheckboxInput(attrs={'placeholder': 'Private', 'label': 'Private'}))

  class Meta:
    model = List
    fields = ('description', 'private')


class NewKitchenForm(KitchenEditForm):
  title = forms.CharField(
    max_length=50,
    help_text='',
    label='Title',
    required=True,
    label_suffix="",
    widget=forms.TextInput(attrs={'placeholder': 'Title'}))

  class Meta:
    model = List
    fields = ('title', 'description', 'private',)

class ItemForm(ModelForm):
  name = forms.CharField(
    max_length=30,
    label='Item Name',
    required=True,
    label_suffix="",
    widget=forms.TextInput(attrs={'placeholder': 'Item'}))
  status = forms.ChoiceField(
    choices=ITEM_STATUS,
    label='Status',
    label_suffix="",
    widget=forms.Select(attrs={'placeholder': 'Status'}) )
  notes = forms.CharField(
    max_length=100,
    help_text='',
    label='Notes',
    required=False,
    label_suffix="",
    widget=forms.Textarea(attrs={'placeholder': 'Notes', }))

  class Meta:
    model = Item
    fields = ('name', 'status', 'notes',)

class ItemEditForm(ModelForm):
  notes = forms.CharField(
    max_length=100,
    help_text='',
    label='Notes',
    required=True,
    label_suffix="",
    widget=forms.Textarea(attrs={'placeholder': 'Notes', }))

  class Meta:
    model = Item
    fields = ('notes',)