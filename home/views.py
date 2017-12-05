from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User
from todolists.core.forms import UserRegistrationForm, UserLoginForm
from list.models import List


def index(request):
  kitchens = List.objects.filter(private=False, deleted=False)
  if request.user.is_authenticated():
    user = request.user
  else:
    user = None
  return render(request, 'home/index.html', { 'user': user, 'kitchens': kitchens })


def register(request):
  registration_form = UserRegistrationForm()
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.refresh_from_db()
      user.profile.birth_date = form.cleaned_data.get('birth_date')
      user.profile.bio = form.cleaned_data.get('bio')
      user.save()
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=user.username, password=raw_password)
      user_login(request, user)
      return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))
    else:
      return render(request, 'home/register.html', {'registration_form': form })
  else:
    return render(request, 'home/register.html', { 'registration_form': registration_form })


def login(request):
  login_form = UserLoginForm()
  if request.method == "POST":
    form = UserLoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        user_login(request, user)
        return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))
      else:
        return render(request, 'home/login.html', { 'login_form': form })
    else:
      return render(request, 'home/login.html', { 'login_form': form })
  else:
    return render(request, 'home/login.html', {'login_form': login_form })


def logout(request):
  user_logout(request)
  return HttpResponseRedirect(reverse('home:index'))


def about(request):
  return render(request, 'home/about.html')