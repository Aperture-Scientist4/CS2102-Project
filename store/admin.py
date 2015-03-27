from django.contrib import admin
from store.models import Rent, Purchased, App
from django.contrib.auth.models import User

admin.site.register(Rent)
admin.site.register(Purchased)
admin.site.register(App)

