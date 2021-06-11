from django.contrib import admin

from .models import User

# Register your models here.

class showEmails(admin.ModelAdmin):
    list_display = ["user", "sender", "subject", "body", "read", "archived"]

    

admin.site.register(User)