from django.contrib import admin
from .models import Pizza, Toppings, Dough, Snacks, Desserts, Drinks

# Register your models here.

admin.site.register(Pizza)
admin.site.register(Toppings)
admin.site.register(Dough)
admin.site.register(Snacks)
admin.site.register(Drinks)
admin.site.register(Desserts)