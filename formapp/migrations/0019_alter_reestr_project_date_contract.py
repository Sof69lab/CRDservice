# Generated by Django 4.1 on 2023-12-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0018_alter_reestr_customer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reestr",
            name="project_date_contract",
            field=models.DateField(blank=True, null=True, verbose_name="Дата договора"),
        ),
    ]