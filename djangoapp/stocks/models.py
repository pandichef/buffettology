from django.db import models
from django.db.models import QuerySet, Sum, Count, ExpressionWrapper
from django.db.models import (
    F,
    Case,
    When,
    Value,
    CharField,
    Q,
    FloatField,
    DecimalField,
    TextField,
    URLField,
)
from django.db.models.functions import Round, Concat, Coalesce
from django.conf import settings
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError

import os
import pandas as pd
from datetime import datetime
import os
import pickle
from .add_qt_pd import add_qt_pd
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io

import concurrent.futures
from django.contrib import messages
from .prompts import (
    boolean_suffix,
    fisher_prompts,
    eps_estimate_y10_prompt,
)
from .llm_utils import (
    fetch_llm_completion,
    extract_completion_boolean,
    extract_completion_float,
)
from .validators import validate_parquet_file
from .gsheet_utils import create_google_sheet
from .sip_data_dictionary import sip_data_dictionary


class Stock(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticker = models.CharField(max_length=7, unique=False)
    google_sheet_url = URLField(null=True)
    conclusion = HTMLField(blank=True, null=True)
    psd_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        unique=False,
        verbose_name="Price",
    )
    ee_eps_ey0 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        unique=False,
        verbose_name="EPS Est Y0",
    )
    qt_pd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        unique=False,
        verbose_name="Quant PD (%)",
    )
    eps_estimate_y10 = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=10,
        verbose_name="LLM EPS Est Y10",
    )
    eps_estimate_y10_completion = TextField(
        blank=True, null=True, verbose_name="LLM EPS Est Y10 Analysis"
    )
    fisher1 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[0])
    fisher1_completion = TextField(blank=True, null=True)
    fisher2 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[1])
    fisher2_completion = TextField(blank=True, null=True)
    fisher3 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[2])
    fisher3_completion = TextField(blank=True, null=True)
    fisher4 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[3])
    fisher4_completion = TextField(blank=True, null=True)
    fisher5 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[4])
    fisher5_completion = TextField(blank=True, null=True)
    fisher6 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[5])
    fisher6_completion = TextField(blank=True, null=True)
    fisher7 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[6])
    fisher7_completion = TextField(blank=True, null=True)
    fisher8 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[7])
    fisher8_completion = TextField(blank=True, null=True)
    fisher9 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[8])
    fisher9_completion = TextField(blank=True, null=True)
    fisher10 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[9])
    fisher10_completion = TextField(blank=True, null=True)
    fisher11 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[10])
    fisher11_completion = TextField(blank=True, null=True)
    fisher12 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[11])
    fisher12_completion = TextField(blank=True, null=True)
    fisher13 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[12])
    fisher13_completion = TextField(blank=True, null=True)
    fisher14 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[13])
    fisher14_completion = TextField(blank=True, null=True)
    fisher15 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[14])
    fisher15_completion = TextField(blank=True, null=True)

    # from django.contrib import messages
    def setattr_from_sip(self, fieldname, df):
        value = float(df[fieldname][self.ticker])
        if not getattr(self, fieldname) and not pd.isnull(value):
            setattr(self, fieldname, float(df[fieldname][self.ticker]))

    def save(self, *args, request=None, **kwargs):
        if self.ticker:
            self.ticker = self.ticker.upper()

        # get SIP data
        try:
            sip_file_path = os.path.join(
                settings.MEDIA_ROOT, datetime.now().strftime("%Y%m%d") + ".parquet"
            )
            sip_df = pd.read_parquet(sip_file_path)

            for field in ["psd_price", "ee_eps_ey0", "qt_pd"]:
                self.setattr_from_sip(field, sip_df)
        except Exception as e:
            if request is not None:
                messages.error(
                    request, f"An error occurred while processing the file: {e}"
                )
            return None
            # raise ValidationError(f"An error occurred while processing the file: {e}")

        if not self.eps_estimate_y10_completion:
            self.eps_estimate_y10_completion = fetch_llm_completion(
                eps_estimate_y10_prompt.format(
                    ticker=self.ticker, fisher_prompt0=fisher_prompts[0]
                )
            )
            self.eps_estimate_y10 = extract_completion_float(
                self.eps_estimate_y10_completion
            )

        # Use multithreading to process fisher analyses
        def process_fisher(i):
            analysis_field = f"fisher{i}_completion"
            fisher_field = f"fisher{i}"
            # print(getattr(self, analysis_field))
            if not getattr(self, analysis_field):
                # print("analysis_field")
                analysis = fetch_llm_completion(
                    f"For ticker {self.ticker}, {fisher_prompts[i-1]}"
                    + " "
                    + boolean_suffix
                )
                setattr(self, analysis_field, analysis)
                setattr(self, fisher_field, extract_completion_boolean(analysis))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_fisher, i) for i in range(1, 16)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception in thread: {e}")

        # sip_df = sip_df.rename(columns=sip_data_dictionary)
        this_stock_data = sip_df.transpose()[[self.ticker]]
        this_stock_data = this_stock_data.reset_index(drop=False)
        this_stock_data = this_stock_data.rename(
            columns={"index": "name", self.ticker: "value"}
        )
        this_stock_data["description"] = this_stock_data["name"].map(
            sip_data_dictionary
        )
        self.google_sheet_url = create_google_sheet(self.ticker, this_stock_data)

        super().save(*args, **kwargs)

    class CustomManager(models.Manager):
        def get_queryset(self):
            fisher_field_list = [f"fisher{i}" for i in range(1, 16)]
            return (
                super()
                .get_queryset()
                .annotate(
                    price_in_y10=Value(20) * F("eps_estimate_y10"),
                    long_term_irr=Concat(
                        Round(
                            Value(100)
                            * (
                                (F("price_in_y10") / F("psd_price"))
                                ** Value(0.10, output_field=DecimalField())
                                - 1
                            ),
                            2,
                        ),
                        Value(""),
                        output_field=models.CharField(),
                    ),
                    true_count=Sum(
                        sum(Coalesce(F(field), 0.0) for field in fisher_field_list),
                        output_field=FloatField(),
                    ),
                    not_null_count=Sum(
                        sum(
                            Case(
                                When(~Q(**{field: None}), then=Value(1)),
                                default=Value(0),
                                output_field=FloatField(),
                            )
                            for field in fisher_field_list
                        ),
                        output_field=FloatField(),
                    ),
                    pr_downside_decimal=Round(
                        100 - Value(100) * F("true_count") / F("not_null_count"), 2,
                    ),
                    pr_downside=Concat(
                        F("pr_downside_decimal"),
                        Value(""),
                        output_field=models.CharField(),
                    ),
                    combined_default_probability_decimal=Round(
                        Value(0.50) * (F("qt_pd") + F("pr_downside_decimal")),
                        2,
                        output_field=models.DecimalField(),
                    ),
                    combined_default_probability=Concat(
                        F("combined_default_probability_decimal"),
                        Value(""),
                        output_field=models.CharField(),
                    ),
                )
            )

    objects = CustomManager()

    def __str__(self):
        return f"{str(self.ticker)}"


########################################################################################
def use_date_as_filename(instance, filename):
    try:
        original_filename = ".".join(filename.split(".")[0:-1])
        datetime.strptime(original_filename, "%Y%m%d")
        return filename
    except ValueError:
        # return False
        new_filename = datetime.now().strftime("%Y%m%d")
        ext = filename.split(".")[-1]
        return f"{new_filename}.{ext}"


class SIPFlatFile(models.Model):
    file = models.FileField(
        upload_to=use_date_as_filename, validators=[validate_parquet_file]
    )
    qt_pd_regression_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{str(self.file.name)}"

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            try:
                old_file = SIPFlatFile.objects.get(pk=self.pk).file
            except SIPFlatFile.DoesNotExist:
                old_file = None

            # If there's an old file and it's not the same as the new one, delete it
            if old_file and self.file != old_file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)

        # Process the new file
        if self.file:
            # Read the uploaded file into a pandas DataFrame using an in-memory buffer
            self.file.seek(0)
            buffer = io.BytesIO(self.file.read())
            df = pd.read_parquet(buffer)

            # Add the new column
            df, self.qt_pd_regression_summary = add_qt_pd(df)

            # Save the modified DataFrame to a new in-memory buffer
            modified_buffer = io.BytesIO()
            df.to_parquet(modified_buffer, index=True)
            modified_buffer.seek(0)

            # Save the new file content back to the file field
            self.file.save(
                os.path.basename(self.file.name),
                ContentFile(modified_buffer.read()),
                save=False,
            )

        # Save the new file
        super(SIPFlatFile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the file from storage when the model is deleted
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(SIPFlatFile, self).delete(*args, **kwargs)
