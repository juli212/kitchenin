from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User
from todolists.core.forms import UserRegistrationForm, UserLoginForm
import pdb

def index(request):
  if request.user.is_authenticated():
    user = request.user
  else:
    user = None
  registration_form = UserRegistrationForm()
  login_form = UserLoginForm()
  return render(request, 'home/index.html', {'registration_form': registration_form, 'login_form': login_form, 'user': user })

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.refresh_from_db()
      user.profile.birth_date = form.cleaned_data.get('birth_date')
      user.save()
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=user.username, password=raw_password)
      user_login(request, user)
      return HttpResponseRedirect(reverse('profiles:detail', args=(user.id,)))
  else:
    # pdb.set_trace()
    form = UserRegistrationForm()
    return render(request, 'home/index.html', { 'form': form })

def login(request):
  if request.method == "POST":
    form = UserLoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        user_login(request, user)
        return HttpResponseRedirect(reverse('profiles:detail', args=(user.id,)))
      else:
        return HttpResponse("Login failed")
  else:
    return HttpResponseRedirect(reverse('home:index'))

def logout(request):
  user_logout(request)
  return HttpResponseRedirect(reverse('home:index'))