from __future__ import unicode_literals

from django.db import models

from datetime import datetime

class State(models.Model):
	abbreviation = models.CharField(max_length=2, default='', unique=True)
	name = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return "{}{}".format((self.name[0]).upper(), self.name[1:]);
	
	class Meta:
		ordering = ('name',)

class Candidate(models.Model):
	states = models.ManyToManyField(State)

	first_name = models.CharField(max_length=15, default='')
	last_name = models.CharField(max_length=15, default='', unique=True)

	PARTY_CHOICES = (
		('d', 'democratic'),
		('r', 'republican'),
		('o', 'other')
	)
	party = models.CharField(max_length=1, choices=PARTY_CHOICES, default='o')

	def __unicode__(self):
		return "{} {}".format(self.first_name, self.last_name)


class Tweet(models.Model):
	candidate = models.ForeignKey(Candidate)
	state = models.ForeignKey(State)
	created_at = models.DateField(default=datetime.now)
	author = models.CharField(max_length=50)
	text = models.CharField(max_length=160, unique=True)
	location = models.CharField(max_length=50)
	sentiment = models.DecimalField(max_digits=5, decimal_places=2)

	def __unicode__(self):
		return "{} - {} - {}".format(self.state, self.candidate, self.sentiment)
	
	class Meta:
		ordering = ('state', 'candidate',)
