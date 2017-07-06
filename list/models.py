from django.db import models
from django.utils import timezone
import pdb

class List(models.Model):
	title = models.CharField(max_length=50)
	creator = models.ForeignKey('auth.User', related_name='owned_lists')
	description = models.TextField(blank=True, max_length=100)
	members = models.ManyToManyField('auth.User', related_name='lists')

	def __str__(self):
		return self.title

	def update_item_status(self, item, change):
		if item[1] == True:
			self.items.add(item[0])
			change.old_status = 4
		else:
			last_change = item[0].newest_change()
			last_change.not_newest_change()
			last_change.save()
			change.old_status = last_change.current_status
		return [item[0], change]

# class Reminder(models.Model):
# 	title = models.CharField(max_length=30)
# 	message = models.TextField(blank=True, max_length=200 )
# 	from_user = models.ForeignKey("auth.User", default=1, related_name='from_user')
# 	fridge = models.ForeignKey(List, related_name='reminders')

# 	def __str__(self):
# 		return self.title