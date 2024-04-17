# Generated by Django 4.1 on 2023-12-26 10:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0022_alter_reestr_comment_alter_reestr_labor_costs_plan_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reestr",
            name="comment",
            field=models.TextField(blank=True, verbose_name="10.3. Комментарии"),
        ),
        migrations.AlterField(
            model_name="reestr",
            name="root_cause_list",
            field=models.TextField(blank=True, verbose_name="15. Коренная причина"),
        ),
        migrations.AlterField(
            model_name="reestr",
            name="total_importance",
            field=models.TextField(blank=True, verbose_name="14. Значимость замечания"),
        ),
    ]