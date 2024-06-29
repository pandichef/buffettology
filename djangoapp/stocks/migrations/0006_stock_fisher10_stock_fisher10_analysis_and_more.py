# Generated by Django 4.1 on 2024-06-25 00:20

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0005_stock_fisher1"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="fisher10",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher10_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher11",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher11_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher12",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher12_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher13",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher13_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher14",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher14_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher15",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher15_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher2",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher2_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher3",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher3_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher4",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher4_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher5",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher5_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher6",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher6_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher7",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher7_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher8",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher8_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher9",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="fisher9_analysis",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]