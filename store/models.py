from django.db import models
from django.contrib.auth.models import User


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
	def __str__(self):
		return self.appid
'''
class Customer(models.Model):
	email = models.CharField(max_length=128, primary_key=True)
	password = models.CharField(max_length=128)
	def __str__(self):
		return self.email
	def check_password(self, password):
		return self.password == password
	def retrieve_purchased(self):
		return Purchased.objects.filter(email=self.email)
	def retrieve_rent(self):
		return Rent.objects.filter(email=self.email)
'''
class Purchased(models.Model):
	order_id = models.CharField(max_length=32, primary_key=True)
	username = models.ForeignKey(User)
	appid = models.ForeignKey(App)
	rating = models.PositiveIntegerField(null=True)
	review = models.CharField(max_length=1024, null=True)
	def __str__(self):
		return self.order_id

class Rent(models.Model):
	order_id = models.CharField(max_length=32, primary_key=True)
	username = models.ForeignKey(User)
	appid = models.ForeignKey(App)
	rating = models.PositiveIntegerField(null=True)
	review = models.CharField(max_length=1024, null=True)
	expire_date = models.DateField()
	def __str__(self):
		return self.order_id
