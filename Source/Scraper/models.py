from django.db import models

# model for all competition infos
class Competitions(models.Model):
	league = models.IntegerField(default=0)			# 0:International 1:National
	kind = models.CharField(max_length=50)			# AFC/Arab/CAF/...
	title = models.CharField(max_length=50)			# Asian Cup/AFF U23/...
	session = models.CharField(max_length=50)		# 2017/2017-2018/...

class Matches(models.Model):
	matchno = models.IntegerField(default=0)		# competition number
	date = models.DateTimeField('date published')	# competition date
	hteam = models.CharField(max_length=50)			# home team
	gteam = models.CharField(max_length=50)			# guest team
	hscore = models.CharField(max_length=50)		# home score
	gscore = models.CharField(max_length=50)		# guest score
	haction = models.CharField(max_length=100)		# home score list
	gaction = models.CharField(max_length=100)		# guest score list

# model for country list
class Leagues(models.Model):
	cname = models.CharField(max_length=50)			# country name
	lname = models.CharField(max_length=50)			# league name