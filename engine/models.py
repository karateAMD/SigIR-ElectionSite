from __future__ import unicode_literals

from django.db import models

class State(models.Model):
	abbreviation = models.CharField(max_length=2, default='', unique=True)
	name = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.name.upper();
	
	class Meta:
		ordering = ('name',)

class SearchTerm(models.Model):
	state = models.ForeignKey(State)

	text = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.text
	
	class Meta:
		ordering = ('text',)

class Candidate(models.Model):
	state = models.ManyToManyField(State)

	first_name = models.CharField(max_length=15, default='')
	last_name = models.CharField(max_length=15, default='', unique=True)

	def __unicode__(self):
		return self.first_name + " " + self.last_name


class Tweet(models.Model):
	candidate = models.ForeignKey(Candidate)
	state = models.ForeignKey(State)

	user_id = models.IntegerField(default=0)
	author = models.CharField(max_length=20)
	text = models.CharField(max_length=140)
	location = models.CharField(max_length=50)
	sentiment = models.DecimalField(max_digits=5, decimal_places=2)
