# Generated by Django 4.1 on 2024-06-27 05:17

from django.db import migrations, models
import stocks.models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0007_alter_stock_fisher1_alter_stock_fisher10_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SIPFlatFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to=stocks.models.use_date_as_filename,
                        validators=[stocks.models.validate_parquet_file],
                    ),
                ),
            ],
        ),
    ]
