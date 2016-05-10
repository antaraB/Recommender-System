from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	uname = models.CharField(max_length=100)
	upass = models.CharField(max_length=100)
	age = models.IntegerField(default=18)