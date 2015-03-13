from django.contrib import admin
from store.models import App, User, Purchased, Rent

admin.site.register(App)
admin.site.register(Purchased)
admin.site.register(Rent)
