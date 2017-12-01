from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.exceptions import ValidationError

# from django.utils.deconstruct import deconstructible
# from django.utils.translation import ugettext_lazy as _
# from django.core.validators import BaseValidator
from datetime import date
# import pdb


def AgeValidator(value):
	today = date.today()
	age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
	if age < 18:
		raise ValidationError('Age must be at least 18.')


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=300, blank=True)
	birth_date = models.DateField(null=False, validators=[AgeValidator], default=date.today)

	def __unicode__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
