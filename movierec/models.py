from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	age=models.IntegerField(default=18)
	email=models.CharField( max_length=100)
	password=models.CharField( max_length=100)
	occ=models.CharField(max_length=100)
	pin=models.CharField(max_length=100)
	sex=models.CharField(max_length=2)
	uid=models.IntegerField(default=100)
	def __str__(self):
		return email

class Movie(models.Model):
	movieid=models.IntegerField(default=0)
	mname=models.CharField(max_length=200)
	genre=models.CharField(max_length=200)
	def __str__(self):
		return mname