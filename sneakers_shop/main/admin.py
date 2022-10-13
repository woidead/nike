from django.contrib import admin
from main.models import *

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name')

admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(SneakerCard)