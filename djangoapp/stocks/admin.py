from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    # CustomUser,
    Stock,
)  # Import your model here
from django.db.models import Q
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.db.models import F, Case, When, Value, CharField, Q
from openai import OpenAI, BadRequestError
from django.utils.html import format_html


class StockAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "ticker",
        # "fisher1_analysis",
        "fisher1",
        "fisher2",
        "fisher3",
        "fisher4",
        "fisher5",
        "fisher6",
        "fisher7",
        "fisher8",
        "fisher9",
        "fisher10",
        "fisher11",
        "fisher12",
        "fisher13",
        "fisher14",
        "fisher15",
        # "tmp123",
    )
    search_fields = ("name",)
    # model = Property

    # def map_url(self, obj):
    #     if obj.pin:
    #         return format_html('<a href="{}" target="_blank">{}</a>', obj.pin, obj.pin)
    #     else:
    #         return ""


admin.site.register(Stock, StockAdmin)
