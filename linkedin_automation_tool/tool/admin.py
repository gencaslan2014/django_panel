from django.contrib import admin
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Leads

class LeadAdmin(admin.ModelAdmin):
    pass

admin.site.register(Leads, LeadAdmin)