from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import List
from items.models import Item, Change
from django.contrib.auth.models import User
from todolists.core.forms import KitchenEditForm, ItemForm
import pdb


def index(request):
	return HttpResponseRedirect(reverse('home:index'))


@login_required(redirect_field_name=None, login_url='/')
def detail(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	itemForm = ItemForm()
	if kitchen.deleted == False:
		if user in kitchen.members.all():
			if request.method == 'POST' and KitchenEditForm(request.POST).is_valid():
				kitchen.description = request.POST['description']
				kitchen.private = True if 'private' in request.POST else False
				kitchen.save()
				return HttpResponseRedirect(reverse('lists:detail', args=(kitchen.id, )))
			else:
				return render(request, 'lists/detail.html', { 'kitchen': kitchen, 'item_form': itemForm })
		elif kitchen.private == False:
			return render(request, 'lists/detail.html', { 'kitchen': kitchen })
		else:
			return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def create(request):
	user = request.user
	kitchen = List(title=request.POST['title'], description=request.POST['description'], creator=user)
	kitchen.save()
	kitchen.members.add(user)
	return HttpResponseRedirect(reverse('lists:detail', args=(kitchen.id,)))


@login_required(redirect_field_name=None, login_url='/')
def add_item(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if kitchen.deleted == False and user in kitchen.members.all():
		item_name = request.POST['name'].strip().capitalize()
		item = kitchen.items.get_or_create(name=item_name)
		if item[1] == True:
			item[0].notes = request.POST['notes']
		change = Change(current_status=request.POST['status'], owner = request.user, item = item[0])
		item_and_change = kitchen.update_item_status(item, change)
		item_and_change[0].save()
		item_and_change[1].save()
		return HttpResponseRedirect(reverse('lists:detail', args=(kitchen.id,)))
	else:
		HttpResponseRedirect(reverse('profiles:detail', args=(request.user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def members(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if user in kitchen.members.all():
		return render(request, 'lists/members.html', { 'kitchen': kitchen })
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def find_member(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if kitchen.deleted == False and user in kitchen.members.all():
		if request.method == "POST":
			query = request.POST['user-search'].strip()
			search_results = User.objects.filter(username__icontains=query)
			return render(request, 'lists/find_member.html', {'kitchen': kitchen, 'results': search_results})
		else:
			return render(request, 'lists/find_member.html', { 'kitchen': kitchen})
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def add_member(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if kitchen.deleted == False and user in kitchen.members.all():
		if request.method == "POST":
			name = request.POST['username']
			new_member = get_object_or_404(User, username=name)
			if new_member not in kitchen.members.all():
				kitchen.members.add(new_member)
			return HttpResponseRedirect(reverse('lists:members', args=(kitchen.id,)))
		else:
			return HttpResponseRedirect(reverse('lists:find_member', args=(kitchen.id,)))
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def remove_member(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if kitchen.deleted == False and user in kitchen.members.all():
		if request.method == "POST":
			name = request.POST['username']
			member_to_remove = get_object_or_404(User, username=name)
			if member_to_remove in kitchen.members.all():
				kitchen.members.remove(member_to_remove)
		return HttpResponseRedirect(reverse('lists:members', args=(kitchen.id,)))
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def leave_list(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if (kitchen.deleted == False and user in kitchen.members.all() and user != kitchen.creator):
		kitchen.members.remove(user)
	return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def edit(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if kitchen.deleted == False and user == kitchen.creator:
		kitchenForm = KitchenEditForm(instance=kitchen)
		return render(request, 'lists/edit.html', {'kitchen': kitchen, 'form': kitchenForm})
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def destroy(request, list_id):
	kitchen = get_object_or_404(List, pk=list_id)
	user = request.user
	if kitchen.deleted == False and user == kitchen.creator:
		kitchen.deleted = True
		kitchen.save()
	return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))