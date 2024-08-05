import os
import pandas as pd
from datetime import datetime
from django.conf import settings
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.db.models import F, Case, When, Value, CharField, Q
from django.utils.html import format_html
from django.shortcuts import render
from django import forms
from django.utils.safestring import mark_safe
import markdown2
from openai import OpenAI, BadRequestError
from .models import (
    # CustomUser,
    Stock,
    SIPFlatFile,
    CustomField,
)  # Import your model here


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


class CustomFieldInline(admin.TabularInline):
    template = "admin/stocks/custom_tabular.html"
    can_delete = False
    model = CustomField
    fields = ["name", "description"]
    readonly_fields = ["name", "description"]
    extra = 0
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


class SIPFlatFileAdmin(admin.ModelAdmin):
    inlines = [CustomFieldInline]


class StockAdmin(admin.ModelAdmin):
    change_list_template = "admin/stocks/stock_changelist.html"

    def has_add_permission(self, request):
        # Disable the 'Add' button for all users
        # use bulk create button instead
        return False

    def changelist_view(self, request, extra_context=None):
        form = BulkCreateForm()
        print(request.POST.get("value"))
        if request.method == "POST" and request.POST.get("value") == "Bulk Add":
            form = BulkCreateForm(request.POST)
            if form.is_valid():
                tickers = form.cleaned_data["tickers"]
                ticker_list = [ticker.strip() for ticker in tickers.split(",")]

                # Create Stock instances using Stock.objects.create()
                # created_objects = []
                for ticker in ticker_list:
                    stock = Stock.objects.create(ticker=ticker)
                    # created_objects.append(stock)

                self.message_user(request, "Objects created successfully!")
                return HttpResponseRedirect(request.path)
        # if request.method == "POST" and request.POST.get("value") == "Add 5 More Leads":
        #     try:
        #         sip_file_path = os.path.join(
        #             settings.MEDIA_ROOT, datetime.now().strftime("%Y%m%d") + ".parquet"
        #         )
        #         sip_df = pd.read_parquet(sip_file_path)
        #         sip_df = sip_df.dropna(subset=["qt_pd"])
        #         sip_df = sip_df.sort_values(by="qt_pd", ascending=True)
        #         ticker_list = list(sip_df.index)[0:5]
        #         for ticker in ticker_list:
        #             stock = Stock.objects.create(ticker=ticker)
        #         self.message_user(request, ",".join(ticker_list))
        #         return HttpResponseRedirect(request.path)
        #     except Exception as e:
        #         self.message_user(
        #             request, f"An error occurred while processing the file: {e}"
        #         )

        extra_context = extra_context or {}
        extra_context["form"] = form
        return super().changelist_view(request, extra_context=extra_context)

    list_display = (
        "created_at",
        "ticker",
        # "psd_price",
        # "fisher1_analysis",
        # "ee_eps_ey0",
        "eps_estimate_y10",
        # "price_in_y10",
        # "long_term_irr",
        # "true_count",
        # "not_null_count",
        "pr_downside",
        # "qt_pd",
        # "combined_default_probability",
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
    exclude = ("id",)

    ################
    # MARKDOWN HACKS
    def get_fields(self, request, obj=None):
        # This is needed to preserve the ORDERING of markdown fields
        all_fields = [field.name for field in self.model._meta.fields]
        updated_strings = [
            s.replace("_completion", "_rendered") if s.endswith("_completion") else s
            for s in all_fields
        ]
        # updated_strings = [
        #     s.replace("google_sheet_url", "google_sheet") for s in all_fields
        # ]
        updated_strings = [
            "google_sheet" if item == "google_sheet_url" else item
            for item in updated_strings
        ]
        updated_strings.remove("id")
        updated_strings.remove("ticker")
        return updated_strings

    def get_readonly_fields(self, request, obj=None):
        # This is hacky; required because Django throws an error if non-editable fields
        # are not in the readonly return value
        non_editable_fields = ["id"] + [
            field.name for field in self.model._meta.get_fields() if not field.editable
        ]
        all_fields = self.get_fields(request, obj)
        rendered_fields = [field for field in all_fields if field.endswith("_rendered")]
        return (
            non_editable_fields
            + rendered_fields
            + [
                "ticker",
                # "psd_price",
                # "ee_eps_ey0",
                # "qt_pd",
                "eps_estimate_y10",
                "google_sheet",
                "ci_company",
            ]
        )

    for i in range(1, 16):
        func_code = f"""
def fisher{i}_rendered(self, obj):
    if obj.fisher{i}_completion:
        return mark_safe(markdown2.markdown(obj.fisher{i}_completion))
    return ""
"""
        exec(func_code)

    def eps_estimate_y10_rendered(self, obj):
        if obj.eps_estimate_y10_completion:
            return mark_safe(markdown2.markdown(obj.eps_estimate_y10_completion))
        return ""

    ##################
    # ANNOTATION HACKS
    # def price_in_y10(self, obj):
    #     return obj.price_in_y10

    # def long_term_irr(self, obj):
    #     return obj.long_term_irr

    # long_term_irr.short_description = "LT IRR (%)"

    def pr_downside(self, obj):
        return obj.pr_downside

    pr_downside.short_description = "Qualitative PD (%)"

    def combined_default_probability(self, obj):
        return obj.combined_default_probability

    combined_default_probability.short_description = "Combo PD (%)"

    #############
    # OTHER HACKS
    def google_sheet(self, obj):
        # Because URLField text appears as raw text in readonly mode
        if obj.google_sheet_url:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.google_sheet_url,
                obj.google_sheet_url,
            )
        return "-"

    google_sheet.short_description = "Google Sheet"


admin.site.register(Stock, StockAdmin)
admin.site.register(SIPFlatFile, SIPFlatFileAdmin)


class CustomFieldAdmin(admin.ModelAdmin):
    exclude = ["details"]
    readonly_fields = ["sip_flat_file", "name", "description", "details_"]

    def details_(self, obj):
        return format_html(f"<pre>{obj.details}</pre>")

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None) -> bool:
        return False


admin.site.register(CustomField, CustomFieldAdmin)
