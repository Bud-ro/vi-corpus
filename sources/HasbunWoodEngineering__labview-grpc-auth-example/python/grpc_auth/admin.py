from django.contrib import admin
from .models import DeviceLinkSession


@admin.register(DeviceLinkSession)
class DeviceLinkSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "used",
        "created_at",
        "expires_at",
    )
    list_filter = ("used",)
    search_fields = ("user__email", "user__username", "id")
