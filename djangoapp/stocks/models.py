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
)
from django.db.models.functions import Round, Concat, Coalesce
from django.conf import settings
from tinymce.models import HTMLField

# from django.conf import settings
import os
import pandas as pd
from datetime import datetime
from django.core.exceptions import ValidationError
import os
import pickle
import concurrent.futures
from django.contrib import messages

prompt_suffix_skeptical_boolean_result = """Be skeptical in your response.  
If the final answer is "Yes", then the response must end in the string "Conclusion: Yes".  
If the final answer is "No", then the response must end in the string "Conclusion: No".
Do not use any markdown text in the reponse."""

fisher_prompts = [
    """Does the company have products or services with sufﬁcient market potential to make possible a sizable increase in sales for at least several years?  In this analysis, consider factors like market share, international growth, and cross-selling opportunities?""",
    """Does the management have a determination to continue to develop products or processes that will still further increase total sales potentials when the growth potentials of currently attractive product lines have largely been exploited?""",
    """How effective are the company’s research and development efforts in relation to its size?""",
    """Does the company have an above-average sales organization?""",
    """Does the company have a worthwhile profit margin?""",
    """What is the company doing to maintain or improve profit margins?""",
    """Does the company have outstanding labor and personnel relations?""",
    """Does the company have outstanding executive relations?""",
    """Does the company have depth to its management?""",
    """How good are the company’s cost analysis and accounting controls?""",
    """Are there other aspects of the business, somewhat peculiar to the industry involved, which will give the investor important clues as to how outstanding the company may be in relation to its competition?""",
    """Does the company have a short-range or long-range outlook in regard to profits?""",
    """In the foreseeable future will the growth of the company require sufﬁcient equity ﬁnancing so that the larger number of shares then outstanding will largely cancel the existing stockholders’ beneﬁt from this anticipated growth?""",
    """Does the management talk freely to investors about its affairs when things are going well but “clam up” when troubles and disappointments occur?""",
    """Does the company have a management of unquestionable integrity?""",
]


def fetch_llm_completion(prompt):
    try:
        from openai import OpenAI

        client = OpenAI()

        completion = client.chat.completions.create(
            model=settings.BASE_OPENAI_MODEL,
            messages=[
                {"role": "system", "content": settings.SYSTEM_CONTENT},
                {"role": "user", "content": prompt,},
            ],
        )
        return str(completion.choices[0].message.content)
    except Exception as e:
        return str(e)


def get_analysis_boolean(analysis_text: str) -> bool | None:
    parsed_analysis_text = analysis_text.split()
    if (
        parsed_analysis_text[-2] == "Conclusion:"
        and parsed_analysis_text[-1].rstrip(".") == "Yes"
    ):
        return True
    elif (
        parsed_analysis_text[-2] == "Conclusion:"
        and parsed_analysis_text[-1].rstrip(".") == "No"
    ):
        return False
    else:
        return None


def get_analysis_float(analysis_text: str) -> float | None:
    parsed_analysis_text = analysis_text.split()
    if parsed_analysis_text[-2] == "Conclusion:":
        try:
            return float(parsed_analysis_text[-1].rstrip(".").lstrip("$"))
        except:
            return None
    else:
        return None


class Stock(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticker = models.CharField(max_length=7, unique=False)
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
    default_prediction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        unique=False,
        verbose_name="Quant PD (%)",
    )
    eps_estimate_y10 = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=10
    )
    eps_estimate_y10_analysis = HTMLField(
        blank=True, null=True, verbose_name="LLM EPS EST Y10"
    )
    fisher1 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[0])
    fisher1_analysis = HTMLField(blank=True, null=True)
    fisher2 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[1])
    fisher2_analysis = HTMLField(blank=True, null=True)
    fisher3 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[2])
    fisher3_analysis = HTMLField(blank=True, null=True)
    fisher4 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[3])
    fisher4_analysis = HTMLField(blank=True, null=True)
    fisher5 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[4])
    fisher5_analysis = HTMLField(blank=True, null=True)
    fisher6 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[5])
    fisher6_analysis = HTMLField(blank=True, null=True)
    fisher7 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[6])
    fisher7_analysis = HTMLField(blank=True, null=True)
    fisher8 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[7])
    fisher8_analysis = HTMLField(blank=True, null=True)
    fisher9 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[8])
    fisher9_analysis = HTMLField(blank=True, null=True)
    fisher10 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[9])
    fisher10_analysis = HTMLField(blank=True, null=True)
    fisher11 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[10])
    fisher11_analysis = HTMLField(blank=True, null=True)
    fisher12 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[11])
    fisher12_analysis = HTMLField(blank=True, null=True)
    fisher13 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[12])
    fisher13_analysis = HTMLField(blank=True, null=True)
    fisher14 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[13])
    fisher14_analysis = HTMLField(blank=True, null=True)
    fisher15 = models.BooleanField(blank=True, null=True, help_text=fisher_prompts[14])
    fisher15_analysis = HTMLField(blank=True, null=True)

    # from django.contrib import messages

    def save(self, *args, request=None, **kwargs):
        if self.ticker:
            self.ticker = self.ticker.upper()

        # get SIP data
        try:
            sip_file_path = os.path.join(
                settings.MEDIA_ROOT, datetime.now().strftime("%Y%m%d") + ".parquet"
            )
            sip_df = pd.read_parquet(sip_file_path)
            if not self.psd_price:
                self.psd_price = float(sip_df["psd_price"][self.ticker])
            if not self.ee_eps_ey0:
                self.ee_eps_ey0 = float(sip_df["ee_eps_ey0"][self.ticker])
            if not self.default_prediction:
                self.default_prediction = float(
                    sip_df["default_prediction"][self.ticker]
                )
        except Exception as e:
            if request is not None:
                messages.error(
                    request, f"An error occurred while processing the file: {e}"
                )

        self.eps_estimate_y10_analysis = fetch_llm_completion(
            f"""
For ticker {self.ticker}, {fisher_prompts[0]}.  
Use this analysis to estimate the EPS of the company 10 years from now.
Be skeptical in your response.  The response must end in a specific number.
For example, if the EPS in year 10 is 2.999, then the response must end in the 
string "Conclusion: 2.999".  Do not use any markdown text in the reponse and 
do not end the response with a period character.
"""
        )
        self.eps_estimate_y10 = get_analysis_float(self.eps_estimate_y10_analysis)

        # Use multithreading to process fisher analyses
        def process_fisher(i):
            analysis_field = f"fisher{i}_analysis"
            fisher_field = f"fisher{i}"
            # print(getattr(self, analysis_field))
            if not getattr(self, analysis_field):
                analysis = fetch_llm_completion(
                    f"For ticker {self.ticker}, {fisher_prompts[i-1]}"
                    + " "
                    + prompt_suffix_skeptical_boolean_result
                )
                setattr(self, analysis_field, analysis)
                setattr(self, fisher_field, get_analysis_boolean(analysis))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_fisher, i) for i in range(1, 16)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception in thread: {e}")

        super().save(*args, **kwargs)

    # pe_in_y10 = 20

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
                        Value(0.50)
                        * (F("default_prediction") + F("pr_downside_decimal")),
                        2,
                        output_field=models.DecimalField(),
                    ),
                    combined_default_probability=Concat(
                        F("combined_default_probability_decimal"),
                        Value(""),
                        output_field=models.CharField(),
                    ),
                    # ExpressionWrapper(
                    #     Value(100) * F("true_count") / F("not_null_count"),
                    #     output_field=FloatField(),
                    # ),
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


def validate_parquet_file(value):
    try:
        # Read the file content and attempt to load it with pandas
        value.seek(0)  # Ensure we start reading from the beginning of the file
        pd.read_parquet(value)  # Will fail if not a valid Parquet file
    except (ValueError, OSError) as e:
        raise ValidationError("This file is not a valid Parquet file.") from e

    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in [".parquet"]:
        raise ValidationError(
            f"Unsupported file extension. Only Parquet files are allowed."
        )


class SIPFlatFile(models.Model):
    file = models.FileField(
        upload_to=use_date_as_filename, validators=[validate_parquet_file]
    )

    def __str__(self):
        return f"{str(self.file.name)}"
