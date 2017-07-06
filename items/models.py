from django.db import models
from django.utils import timezone

from list.models import List

NEED = 1
PANTRY = 2
FRIDGE = 3
GONE = 4
ITEM_STATUS = (
	(NEED, 'need'),
	(PANTRY, 'pantry'),
	(FRIDGE, 'fridge'),
	(GONE, 'gone'),
)
class Item(models.Model):
	added_by = models.ForeignKey("auth.User", related_name='added_by', default=1)
	name = models.CharField(max_length=30)
	notes = models.TextField(blank=True, max_length=200)
	created_date = models.DateTimeField(default=timezone.now)
	kitchen = models.ForeignKey(List, related_name='items')

	def save(self, *args, **kwargs):
		for field_name in ['name']:
			val = getattr(self, field_name, False)
			if val:
				setattr(self, field_name, val.strip().capitalize())
		super(Item, self).save(*args, **kwargs)

	def newest_change(self):
		change = self.item_changes.get(latest_change=True)
		return change

	def status(self):
		status = self.newest_change().current_status
		return status

	def add_item(self):
		self.added_date = timezone.now()
		self.save()

	def display_status(self):
		s = self.status()
		if s == 1:
			return "need"
		elif s == 2:
			return "pantry"
		elif s == 3:
			return "fridge"
		elif s == 4:
			return "gone"

	def last_updated_by(self):
		return self.newest_change().owner

	def update_status(self, new_status, user):
		status = None
		if (new_status == "need") or (new_status == "1"):
			status = 1
		elif (new_status == "pantry") or (new_status == "2"):
			status = 2
		elif (new_status == "fridge") or (new_status == "3"):
			status = 3
		elif (new_status == "gone") or (new_status == "4"):
			status = 4
		change = Change(old_status = self.status(), current_status =status, item = self, owner = user)
		return change

	def __str__(self):
		return self.name

class Change(models.Model):
	old_status = models.IntegerField(choices=ITEM_STATUS, blank=True)
	current_status = models.IntegerField(choices=ITEM_STATUS, default=NEED)
	latest_change = models.BooleanField(default=True)
	date = models.DateTimeField(default=timezone.now)
	item = models.ForeignKey(Item, related_name='item_changes')
	owner = models.ForeignKey("auth.user", related_name='user_changes')

	def kitchen(self):
		return self.item.kitchen

	def not_newest_change(self):
		self.latest_change = False
		self.save()