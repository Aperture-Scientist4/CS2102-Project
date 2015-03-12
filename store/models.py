from django.db import models

class App(models.Model):
	GENRE_CHOICES = (
		('G','Game'),
		('M','Movie'),
		('A',"App"),
		('T',"TV Show")
	)
	appid = models.PositiveIntegerField(primary_key=True)
	name = models.CharField(max_length=32)
	icon = models.CharField(max_length=128, null=True)
	purchase_price = models.PositiveIntegerField()
	rent_price = models.PositiveIntegerField(null=True)
	description = models.CharField(max_length=256)
	device = models.CharField(max_length=128)
	release_date = models.DateField()
	genre = models.CharField(max_length=1, choices=GENRE_CHOICES)

class User(models.Model):
	email = models.CharField(max_length=128, primary_key=True)
	password = models.CharField(max_length=128)

class purchase(models.Model):
	email = models.ForeignKey(User, primary_key=True)
	appid = models.ForeignKey(App, primary_key=True)
	rating = models.PositiveIntegerField(null=True)
	review = models.CharField(max_length=1024, null=True)

class rent(models.Model):
	email = models.ForeignKey(User, primary_key=True)
	appid = models.ForeignKey(App, primary_key=True)
	rating = models.PositiveIntegerField(null=True)
	review = models.CharField(max_length=1024, null=True)
	expire_date = models.DateField()
