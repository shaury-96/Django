from django.contrib import admin
from userauth.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display=['email','first_name','last_name','phone_number']

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)