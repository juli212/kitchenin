from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Profile
# import pdb

@login_required(redirect_field_name=None, login_url='/')
def detail(request, profile_id):
	profile = get_object_or_404(Profile, pk=profile_id)
	return render(request, 'profiles/detail.html', {'profile': profile })