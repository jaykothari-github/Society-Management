from django.contrib import admin
from SecApp.models import *

# Register your models here.

@admin.register(SecUser)
class ModelSecUser(admin.ModelAdmin):

    list_display = ['name','email','mobile','id']

@admin.register(Emergency)
class ModelEmergency(admin.ModelAdmin):

    list_display = ['name','email','mobile','occupation']

