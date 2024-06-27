from django.db import models
from django.db.models import QuerySet
from django.db.models import F, Case, When, Value, CharField, Q
from django.conf import settings
from tinymce.models import HTMLField


class Property(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    notes = HTMLField(default="")
    pin = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return f"{str(self.name)}"


class Document(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    property = models.ForeignKey(Property, on_delete=models.PROTECT,)
    type = models.PositiveSmallIntegerField(
        # max_length=2,
        choices=[(0, "Appraisal"), (1, "Income Statement"), (2, "Bank Statement"),],
        default=0,
    )
    file = models.FileField(upload_to="")
