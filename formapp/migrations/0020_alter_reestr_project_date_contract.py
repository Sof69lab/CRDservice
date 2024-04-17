# Generated by Django 4.1 on 2023-12-08 12:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0019_alter_reestr_project_date_contract"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reestr",
            name="project_date_contract",
            field=models.DateField(
                blank=True,
                default=django.utils.timezone.now,
                verbose_name="Дата договора",
            ),
            preserve_default=False,
        ),
    ]