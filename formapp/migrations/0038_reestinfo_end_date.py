# Generated by Django 4.1 on 2024-03-04 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0037_reestinfo_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="reestinfo",
            name="end_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
