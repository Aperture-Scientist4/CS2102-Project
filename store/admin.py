from django.contrib import admin
from store.models import App, Customer, Purchased, Rent

admin.site.register(App)
admin.site.register(Customer)
admin.site.register(Purchased)
admin.site.register(Rent)
