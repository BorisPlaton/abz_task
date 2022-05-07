from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['password']
