# Generated by Django 4.1 on 2024-06-28 16:43

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0010_alter_stock_fisher1_alter_stock_fisher11_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="eps_estimate_y10_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="stock",
            name="fisher1",
            field=models.BooleanField(
                blank=True,
                help_text="Does the company have products or services with sufﬁcient market potential to make possible a sizable increase in sales for at least several years?  In this analysis, consider factors like market share, international growth, and cross-selling opportunities?",
                null=True,
            ),
        ),
    ]
