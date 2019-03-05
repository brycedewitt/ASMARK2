from django.contrib import admin

# Register your models here.
from .models import Beverage,Drink,Pour,User,Order, DrinkType

admin.site.register(Beverage)
admin.site.register(Drink)
admin.site.register(Pour)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(DrinkType)
