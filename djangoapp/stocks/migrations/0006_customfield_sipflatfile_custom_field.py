# Generated by Django 4.0.6 on 2024-08-05 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_alter_stock_fisher1_alter_stock_fisher10_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=255)),
                ('details', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='sipflatfile',
            name='custom_field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sip_flat_files', to='stocks.customfield'),
        ),
    ]