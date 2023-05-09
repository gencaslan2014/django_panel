from django.db import models
from django.db import models
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

# Create your models here.
class Leads(models.Model):
    name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100,default=None)
    first_name = models.CharField(max_length=100,default=None)
    title = models.CharField(max_length=100, default=None,null=True)
    email = models.CharField(max_length=100, default=None,null=True)
    phone_number = models.CharField(max_length=100, default=None,null=True)
    linkedin = models.CharField(max_length=400, default=None,null=True)
    employees = models.CharField(max_length=100, default=None,null=True)
    company_website = models.CharField(max_length=100, default=None,null=True)
    company_name = models.CharField(max_length=100, default=None,null=True)
    location = models.CharField(max_length=100, default=None,null=True)
    linkedin_sales_navigator = models.CharField(max_length=500, default=None,null=True)
