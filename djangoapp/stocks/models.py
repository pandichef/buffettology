from django.db import models
from django.db.models import QuerySet
from django.db.models import F, Case, When, Value, CharField, Q
from django.conf import settings
from tinymce.models import HTMLField
from django.conf import settings
import os
import pandas as pd
from datetime import datetime
from django.core.exceptions import ValidationError
import os
import pickle
import concurrent.futures

prompt_suffix_skeptical_boolean_result = """Be skeptical in your response.  
If the final answer is "Yes", then the response must end in the string "Conclusion: Yes".  
If the final answer is "No", then the response must end in the string "Conclusion: No".
Do not use any markdown text in the reponse."""

fisher_prompts = [
    """Does the company have products or services with sufﬁcient market potential to make possible a sizable increase in sales for at least several years?  In this analysis, consider factors like market share, international growth, and cross-selling opportunities.""",
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
                {
                    "role": "user",
                    "content": prompt + " " + prompt_suffix_skeptical_boolean_result,
                },
            ],
        )
        return str(completion.choices[0].message.content)
    except Exception as e:
        return str(e)


def get_analysis_boolean(analysis_text: str) -> bool | None:
    parsed_analysis_text = analysis_text.split()
    if parsed_analysis_text[-2] == "Conclusion:" and parsed_analysis_text[-1] == "Yes":
        return True
    elif parsed_analysis_text[-2] == "Conclusion:" and parsed_analysis_text[-1] == "No":
        return False
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

    def save(self, *args, **kwargs):
        if self.ticker:
            self.ticker = self.ticker.upper()

        # get price
        try:
            sip_file_path = os.path.join(
                settings.MEDIA_ROOT, datetime.now().strftime("%Y%m%d") + ".pkl"
            )
            sip_df = pd.read_pickle(sip_file_path)
            if not self.psd_price:
                self.psd_price = float(sip_df["psd_price"][self.ticker])
        except:
            pass

        # Use multithreading to process fisher analyses
        def process_fisher(i):
            analysis_field = f"fisher{i}_analysis"
            fisher_field = f"fisher{i}"
            if getattr(self, analysis_field) == "":
                analysis = fetch_llm_completion(
                    f"For ticker {self.ticker}, {fisher_prompts[i-1]}"
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

    def __str__(self):
        return f"{str(self.ticker)}"


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
