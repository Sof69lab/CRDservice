# Generated by Django 4.1 on 2024-03-13 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0040_alter_reestr_labor_costs_fact_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reestinfo",
            name="add_files",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="uploads/",
                verbose_name="Дополнительные материалы",
            ),
        ),
    ]