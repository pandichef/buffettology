# Generated by Django 4.0.6 on 2024-08-08 05:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_alter_stock_fisher1_alter_stock_fisher10_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sipflatfile',
            name='qt_pd_regression_summary',
        ),
        migrations.AddField(
            model_name='stock',
            name='percentage_true',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.CreateModel(
            name='CustomFieldScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('sip_flat_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.sipflatfile')),
            ],
        ),
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('custom_field_script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.customfieldscript')),
                ('sip_flat_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.sipflatfile')),
            ],
        ),
    ]