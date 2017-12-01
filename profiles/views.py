from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import update_session_auth_hash, authenticate
from todolists.core.forms import UserUpdateEmailForm, UserUpdatePasswordForm, UserUpdateBioForm, UserUpdateNameForm, NewKitchenForm
from .models import Profile
from list.models import List
import pdb


@login_required(redirect_field_name=None, login_url='/')
def detail(request, profile_id):
	profile = get_object_or_404(Profile, pk=profile_id)
	user = request.user
	if request.method == 'POST' and user.profile.id == int(profile_id):
		data = request.POST
		if 'first_name' in data:
			user.first_name = data['first_name']
			user.last_name = data['last_name']
		elif 'email' in data:
			user.email = data['email']
		elif 'current_password' in data and authenticate(username=user.username, password=data['current_password']) == user:
			if data['password1'] == data['password2']:
				user.set_password(data['password1'])
				update_session_auth_hash(request, user)
		elif 'bio' in data:
			user.profile.bio = data['bio']
		user.save()
		return HttpResponseRedirect(reverse('profiles:detail', args=(profile.id,)))
	elif user.profile.id == int(profile_id):
		new_kitchen_form = NewKitchenForm()
		return render(request, 'profiles/detail.html', {'profile': profile, 'kitchen_form': new_kitchen_form, })
	else:
		# kitchens = List.objects.filter(creator=user, deleted=False)
		return render(request, 'profiles/detail.html', {'profile': profile, 'user': user, })


@login_required(redirect_field_name=None, login_url='/')
def edit(request, profile_id):
	user = request.user
	profile = get_object_or_404(Profile, pk=user.profile.id)
	if user.profile.id == int(profile_id):
		nameForm = UserUpdateNameForm(instance=request.user)
		bioForm = UserUpdateBioForm(instance=profile)
		emailForm = UserUpdateEmailForm(instance=request.user)
		passwordForm = UserUpdatePasswordForm()
		newKitchenForm = NewKitchenForm()
		return render(request, 'profiles/editprof.html',{'profile': profile, 'name_form': nameForm, 'bio_form': bioForm, 'email_form': emailForm, 'password_form': passwordForm, 'kitchen_form': newKitchenForm })
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(profile.id,)))