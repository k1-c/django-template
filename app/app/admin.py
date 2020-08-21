from django import forms
from django.contrib import admin
from .models import AppConfig, UserProfile
# Register your models here.


admin.site.register(AppConfig)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "username",
        "birthday",
        "phone_number",
    )

    search_fields = ("user__email", "affiliate_id", "parent__affiliate_id")
