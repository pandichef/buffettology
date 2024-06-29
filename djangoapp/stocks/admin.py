from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    # CustomUser,
    Stock,
    SIPFlatFile,
)  # Import your model here
from django.db.models import Q
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.db.models import F, Case, When, Value, CharField, Q
from openai import OpenAI, BadRequestError
from django.utils.html import format_html
from django.shortcuts import render
from django import forms
from django.utils.safestring import mark_safe

# forms.py
from django import forms


class BulkCreateForm(forms.Form):
    tickers = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "To bulk add stocks, enter comma-separated tickers",
                "rows": 1,
                "cols": 40,
                "style": "width: 80%;",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tickers"].label = False  # Remove the default label rendering


class SIPFlatFileAdmin(admin.ModelAdmin):
    # pass
    readonly_fields = ["quantitative_pd_regression_summary"]
    exclude = ["qt_pd_regression_summary"]

    def quantitative_pd_regression_summary(self, obj):
        return format_html(f"<pre>{obj.qt_pd_regression_summary}</pre>")

    # qt_pd_regression_summary_format_html.long_description = "LT IRR (%)"

    # qt_pd_regression_summary.short_description = "LT IRR (%)"
    # get_qt_pd_regression_summary.allow_tags = True


class StockAdmin(admin.ModelAdmin):
    change_list_template = "admin/stocks/stock_changelist.html"

    def has_add_permission(self, request):
        # Disable the 'Add' button for all users
        # use bulk create button instead
        return False

    def changelist_view(self, request, extra_context=None):
        form = BulkCreateForm()
        if request.method == "POST":
            form = BulkCreateForm(request.POST)
            if form.is_valid():
                tickers = form.cleaned_data["tickers"]
                ticker_list = [ticker.strip() for ticker in tickers.split(",")]

                # Create Stock instances using Stock.objects.create()
                created_objects = []
                for ticker in ticker_list:
                    stock = Stock.objects.create(ticker=ticker)
                    created_objects.append(stock)

                self.message_user(request, "Objects created successfully!")
                return HttpResponseRedirect(request.path)

        extra_context = extra_context or {}
        extra_context["form"] = form
        return super().changelist_view(request, extra_context=extra_context)

    list_display = (
        "created_at",
        "ticker",
        "psd_price",
        # "fisher1_analysis",
        "ee_eps_ey0",
        "eps_estimate_y10",
        "price_in_y10",
        "long_term_irr",
        # "true_count",
        # "not_null_count",
        "pr_downside",
        "qt_pd",
        "combined_default_probability",
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
    search_fields = ("ticker",)

    # def get_queryset(self, request):
    #     return Stock.objects.get_queryset_with_annotations()

    # model = Property
    def price_in_y10(self, obj):
        return obj.price_in_y10

    def long_term_irr(self, obj):
        return obj.long_term_irr

    long_term_irr.short_description = "LT IRR (%)"

    # def true_count(self, obj):
    # return obj.true_count

    # def not_null_count(self, obj):
    # return obj.not_null_count
    def pr_downside(self, obj):
        return obj.pr_downside

    pr_downside.short_description = "Qualitative PD (%)"

    def combined_default_probability(self, obj):
        return obj.combined_default_probability

    combined_default_probability.short_description = "Combo PD (%)"
    # def map_url(self, obj):
    #     if obj.pin:
    #         return format_html('<a href="{}" target="_blank">{}</a>', obj.pin, obj.pin)
    #     else:
    #         return ""
    # def get_queryset(self, request):
    #     return Stock.objects.get_queryset()


admin.site.register(Stock, StockAdmin)
admin.site.register(SIPFlatFile, SIPFlatFileAdmin)
