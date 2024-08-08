# Generated by Django 4.0.6 on 2024-08-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_remove_sipflatfile_qt_pd_regression_summary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfield',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customfieldscript',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='customfield',
            unique_together={('name', 'sip_flat_file')},
        ),
        migrations.AlterUniqueTogether(
            name='customfieldscript',
            unique_together={('name', 'sip_flat_file')},
        ),
    ]
