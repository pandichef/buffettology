# Generated by Django 4.0.6 on 2024-08-04 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_stock_ci_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='ci_company',
            field=models.CharField(max_length=100, null=True, verbose_name='Company name'),
        ),
    ]