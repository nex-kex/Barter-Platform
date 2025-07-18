from django.contrib import admin

from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "title", "description", "category", "condition"
    )
    search_fields = (
        "title",
        "description",
    )
