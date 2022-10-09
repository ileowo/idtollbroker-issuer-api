from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from igrant_user.models import IGrantUser

class IGrantUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'user_type',)

admin.site.register(IGrantUser, IGrantUserAdmin)
