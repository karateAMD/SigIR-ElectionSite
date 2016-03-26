from __future__ import unicode_literals

from django.db import models

class State(models.Model):
	abbreviation = models.CharField(max_length=2, default='')
	name = models.CharField(max_length=200)

class Candidate(models.Model):
	state = models.ForeignKey(State, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)

class Tweet(models.Model):
	candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
	user_id = models.IntegerField(default=0)
	author = models.CharField(max_length=200)
	text = models.CharField(max_length=140)
	location = models.CharField(max_length=50)
