from django.contrib import admin

# Register your models here.
from .models import CustomUser,Car,Model,Sales,Save,Offers
admin.site.register(CustomUser)
admin.site.register(Car)
# admin.site.register(Model)
admin.site.register(Sales)
admin.site.register(Save)
admin.site.register(Offers)
