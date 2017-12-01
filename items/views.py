from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Item, Change
from list.models import List
from django.template.loader import render_to_string
from todolists.core.forms import ItemEditForm
import pdb


@login_required(redirect_field_name=None, login_url='/')
def detail(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	user = request.user
	if user in item.kitchen.members.all():
		if request.method == 'POST':
			new_notes = request.POST['notes']
			item.notes = new_notes
			item.save()
		if request.is_ajax():
			ItemForm = ItemEditForm(instance=item)
			item_detail = render_to_string('items/detail.html', {'item': item, 'notes': item.notes, 'edit_item_form': ItemForm }, request=request)
			return JsonResponse(item_detail, safe=False)
		else:
			return HttpResponseRedirect(reverse('lists:detail', args=(item.kitchen.id,)))
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id,)))


@login_required(redirect_field_name=None, login_url='/')
def move(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	user = request.user
	if user in item.kitchen.members.all():
		previous_new_change = item.newest_change()
		new_change = item.update_status(request.POST['item-status'], user)
		new_change.save()
		previous_new_change.latest_change = False
		previous_new_change.save()
		if request.is_ajax():
			moved_item = render_to_string('lists/kitchen_list.html', {'item': item, 'status': item.status()}, request=request)
			return JsonResponse(moved_item, safe=False)
		else:
			return HttpResponseRedirect(reverse('lists:detail', args=(item.kitchen.id,)))
	else:
		return HttpResponseRedirect(reverse('profiles:detail', args=(user.profile.id)))
