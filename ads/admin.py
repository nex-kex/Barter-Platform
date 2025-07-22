from django.contrib import admin

from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description", "category", "condition")
    search_fields = ("title", "description")
    list_filter = ("condition",)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "ad_sender", "ad_receiver", "status")
    search_fields = ("ad_sender", "ad_receiver")
    list_filter = ("status",)
