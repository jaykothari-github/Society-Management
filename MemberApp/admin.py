from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Member)
class ModelMember(admin.ModelAdmin):
    list_display = ['fname','lname','email','mobile','flat_no','verify']