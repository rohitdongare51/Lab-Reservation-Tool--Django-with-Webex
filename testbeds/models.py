from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Testbed(models.Model):
	device = models.TextField()
	location = models.TextField()
	telnet = models.TextField()
	ssh = models.TextField()	
	notes = models.TextField(default="Add Notes")
	device_type = models.TextField(default="ftd")
	usage = models.TextField(default="notfree")	
	date_posted = models.DateTimeField(auto_now=True)
	testbed_uploader = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.device


	def get_absolute_url(self):
		return reverse('testbed-detail', kwargs={'pk': self.pk})