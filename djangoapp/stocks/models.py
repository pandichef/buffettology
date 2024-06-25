from django.db import models
from django.db.models import QuerySet
from django.db.models import F, Case, When, Value, CharField, Q
from django.conf import settings
from tinymce.models import HTMLField
from django.conf import settings

prompt_suffix = """ Be skeptical in your response.  
If the final answer is "Yes", then the response should end in the string "Conclusion: Yes".  
If the final answer is "No", then the response should end in the string "Conclusion: No".
Do not use any markdown text in the reponse."""


def fetch_llm_completion(prompt):
    try:
        from openai import OpenAI

        client = OpenAI()

        completion = client.chat.completions.create(
            model=settings.BASE_OPENAI_MODEL,
            messages=[
                {"role": "system", "content": settings.SYSTEM_CONTENT},
                {"role": "user", "content": prompt + prompt_suffix},
            ],
        )
        # print("rag_plus_prompt Token count: ", token_count(rag_plus_prompt))
        # print(f"Used {lastest_openai_model} for front-end application")
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
    fisher1_analysis = HTMLField(blank=True, null=True)
    fisher1 = models.BooleanField(blank=True, null=True)
    fisher2_analysis = HTMLField(blank=True, null=True)
    fisher2 = models.BooleanField(blank=True, null=True)
    fisher3_analysis = HTMLField(blank=True, null=True)
    fisher3 = models.BooleanField(blank=True, null=True)
    fisher4_analysis = HTMLField(blank=True, null=True)
    fisher4 = models.BooleanField(blank=True, null=True)
    fisher5_analysis = HTMLField(blank=True, null=True)
    fisher5 = models.BooleanField(blank=True, null=True)
    fisher6_analysis = HTMLField(blank=True, null=True)
    fisher6 = models.BooleanField(blank=True, null=True)
    fisher7_analysis = HTMLField(blank=True, null=True)
    fisher7 = models.BooleanField(blank=True, null=True)
    fisher8_analysis = HTMLField(blank=True, null=True)
    fisher8 = models.BooleanField(blank=True, null=True)
    fisher9_analysis = HTMLField(blank=True, null=True)
    fisher9 = models.BooleanField(blank=True, null=True)
    fisher10_analysis = HTMLField(blank=True, null=True)
    fisher10 = models.BooleanField(blank=True, null=True)
    fisher11_analysis = HTMLField(blank=True, null=True)
    fisher11 = models.BooleanField(blank=True, null=True)
    fisher12_analysis = HTMLField(blank=True, null=True)
    fisher12 = models.BooleanField(blank=True, null=True)
    fisher13_analysis = HTMLField(blank=True, null=True)
    fisher13 = models.BooleanField(blank=True, null=True)
    fisher14_analysis = HTMLField(blank=True, null=True)
    fisher14 = models.BooleanField(blank=True, null=True)
    fisher15_analysis = HTMLField(blank=True, null=True)
    fisher15 = models.BooleanField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.ticker:
            self.ticker = self.ticker.upper()

        ############################
        # FISHER 1
        if self.fisher1_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher1_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the company have 
products or services with sufﬁcient market potential to make possible a 
sizable increase in sales for at least several years?  In this analysis, consider
factors like market share, international growth, and cross-selling opportunities."""
            )
            self.fisher1 = get_analysis_boolean(self.fisher1_analysis)
        ############################
        # FISHER 2
        if self.fisher2_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher2_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the management have a 
determination to continue to develop products or processes that will still 
further increase total sales potentials when the growth potentials of currently 
attractive product lines have largely been exploited?"""
            )
            self.fisher2 = get_analysis_boolean(self.fisher2_analysis)
        ############################
        # FISHER 3
        if self.fisher3_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher3_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, how effective are the company’s 
research and development efforts in relation to its size?"""
            )
            self.fisher3 = get_analysis_boolean(self.fisher3_analysis)
        ############################
        # FISHER 4
        if self.fisher4_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher4_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the company have an above-average sales organization?"""
            )
            self.fisher4 = get_analysis_boolean(self.fisher4_analysis)
        ############################
        # FISHER 5
        if self.fisher5_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher5_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the company have a worthwhile profit margin?"""
            )
            self.fisher5 = get_analysis_boolean(self.fisher5_analysis)
        ############################
        # FISHER 6
        if self.fisher6_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher6_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, what is the company doing to maintain or improve profit margins?"""
            )
            self.fisher6 = get_analysis_boolean(self.fisher6_analysis)
        ############################
        # FISHER 7
        if self.fisher7_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher7_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the company have outstanding labor and personnel relations?"""
            )
            self.fisher7 = get_analysis_boolean(self.fisher7_analysis)
        ############################
        # FISHER 8
        if self.fisher8_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher8_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the company have outstanding executive relations?"""
            )
            self.fisher8 = get_analysis_boolean(self.fisher8_analysis)
        ############################
        # FISHER 9
        if self.fisher9_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher9_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, Does the company have depth to its management?"""
            )
            self.fisher9 = get_analysis_boolean(self.fisher9_analysis)
        ############################
        # FISHER 10
        if self.fisher10_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher10_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, how good are the company’s cost analysis and accounting controls?"""
            )
            self.fisher10 = get_analysis_boolean(self.fisher10_analysis)
        ############################
        # FISHER 11
        if self.fisher11_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher11_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, are there other aspects of the business, 
somewhat peculiar to the industry involved, which will give the investor important 
clues as to how outstanding the company may be in relation to its competition?"""
            )
            self.fisher11 = get_analysis_boolean(self.fisher11_analysis)
        ############################
        # FISHER 12
        if self.fisher12_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher12_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the company have a short-range or long-range outlook in regard to profits?"""
            )
            self.fisher12 = get_analysis_boolean(self.fisher12_analysis)
        ############################
        # FISHER 13
        if self.fisher13_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher13_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, in the foreseeable future will the 
growth of the company require sufﬁcient equity ﬁnancing so that the larger number 
of shares then outstanding will largely cancel the existing stockholders’ beneﬁt 
from this anticipated growth?"""
            )
            self.fisher13 = get_analysis_boolean(self.fisher13_analysis)
        ############################
        # FISHER 14
        if self.fisher14_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher14_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the management talk freely to investors 
about its affairs when things are going well but “clam up” when troubles and disappointments occur?"""
            )
            self.fisher14 = get_analysis_boolean(self.fisher14_analysis)
        ############################
        # FISHER 15
        if self.fisher15_analysis == "":
            # self.fisher1_analysis = self.get_fisher1_analysis(self.ticker)
            self.fisher15_analysis = fetch_llm_completion(
                f"""For ticker {self.ticker}, does the company have a management of unquestionable integrity?"""
            )
            self.fisher15 = get_analysis_boolean(self.fisher15_analysis)

        super().save(*args, **kwargs)

    # class Meta:
    #     verbose_name = "Property"
    #     verbose_name_plural = "Properties"

    def __str__(self):
        return f"{str(self.ticker)}"


# class Document(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     property = models.ForeignKey(Property, on_delete=models.PROTECT,)
#     type = models.PositiveSmallIntegerField(
#         # max_length=2,
#         choices=[(0, "Appraisal"), (1, "Income Statement"), (2, "Bank Statement"),],
#         default=0,
#     )
#     file = models.FileField(upload_to="")


'''
class SourceType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class FineTuningJobManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        qs = qs.annotate(
            job_status=Case(
                When(
                    Q(error_message__isnull=True) & Q(fine_tuned_model__isnull=True),
                    then=Value("Running"),
                ),
                When(
                    Q(error_message__isnull=True) & Q(fine_tuned_model__isnull=False),
                    then=Value("Success"),
                ),
                When(
                    Q(error_message__isnull=False) & Q(fine_tuned_model__isnull=True),
                    then=Value("Failed"),
                ),
                default=Value(
                    "Something went wrong. Error message should be null or Fine-funed should be null"
                ),
                output_field=CharField(),
            )
        )
        return qs


class FineTuningJob(models.Model):
    openai_id = models.CharField(max_length=256, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prior_model = models.CharField(max_length=256, null=False, blank=False)
    # post-completion
    # status = models.CharField(max_length=256, null=True, blank=True)
    error_message = models.CharField(max_length=256, null=True, blank=True)
    fine_tuned_model = models.CharField(max_length=256, null=True, blank=True)

    objects = FineTuningJobManager()

    @classmethod
    def get_latest_openai_model(cls):
        successful_jobs = cls.objects.filter(job_status="Success").order_by(
            "created_at"
        )
        if successful_jobs.count() == 0:
            prior_model = base_openai_model  # settings.BASE_OPENAI_MODEL
            # prior_model = "gpt-4-0613"  # settings.BASE_OPENAI_MODEL
        else:
            last_successful_job = successful_jobs.last()
            prior_model = last_successful_job.fine_tuned_model
        return prior_model

    @classmethod
    def get_lastest_update_date(cls):
        openai_model_name = cls.get_latest_openai_model()
        if openai_model_name == base_openai_model:
            return f"Never updated.  Using {base_openai_model}."
        else:
            last_job = cls.objects.get(fine_tuned_model=openai_model_name)
            return f"Last updated {last_job.updated_at.date()} using base model {base_openai_model}."

    def __str__(self):
        return f"{str(self.openai_id)}"


class Example(models.Model):
    prompt_text = models.TextField()
    completion_text = models.TextField()
    is_approved = models.BooleanField(
        default=False, help_text="Approved for fine-tuning"
    )
    # was_processed = models.BooleanField(
    #     default=False, help_text="Processed in a prior fine-tuning run"
    # )
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_type = models.ForeignKey(
        SourceType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="The source of the record",
    )
    private_reference = models.URLField(
        null=True, blank=True, help_text="Not used in fine-tuning"
    )
    # reference = models.URLField(max_length=200, blank=True)
    private_note = models.TextField(
        null=True, blank=True, help_text="Not used in fine-tuning"
    )
    fine_tuning_job = models.ForeignKey(
        FineTuningJob, on_delete=models.SET_NULL, null=True, blank=True
    )

    @classmethod
    def get_search_results(cls, search_text):
        """
        The following must be run first
        ALTER TABLE base_app_example ADD FULLTEXT INDEX (prompt_text, completion_text);
        See https://database.guide/how-the-match-function-works-in-mysql/
        https://www.promptingguide.ai/techniques/rag

        migrations.RunSQL(
            sql="ALTER TABLE base_app_example ADD FULLTEXT INDEX (prompt_text, completion_text);"
        ), # added to initial migration
        """
        # qs = cls.objects.all()
        # select * from base_app_example where match(prompt_text, completion_text) against('{search_text}')
        search_text = search_text.replace("'", "''")
        minimum_relevance_score = 0
        return Example.objects.raw(
            f"""
SELECT 
  id, MATCH(prompt_text, completion_text) AGAINST('{search_text}') AS relevance
FROM base_app_example
WHERE MATCH(prompt_text, completion_text) AGAINST('{search_text}') > {minimum_relevance_score}
ORDER BY relevance DESC;
"""
        )

    @classmethod
    def get_rag_text(cls, search_text):
        from .finetune import add_context_info

        rawqs = cls.get_search_results(search_text)
        rag_text = ""
        for example in rawqs:
            obj = cls.objects.get(id=example.id)
            rag_text += (
                f"Question: {obj.prompt_text}\nAnswer: {add_context_info(obj)}\n##\n"
            )
        return rag_text

    def __str__(self):
        return (
            f"Example created by {self.created_by.username} on {self.created_at.date()}"
        )
'''
