# Generated by Django 4.1 on 2023-12-26 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0021_alter_reestr_answer_remark_alter_reestr_comment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reestr",
            name="comment",
            field=models.TextField(verbose_name="10.3. Комментарии"),
        ),
        migrations.AlterField(
            model_name="reestr",
            name="labor_costs_plan",
            field=models.FloatField(
                null=True,
                verbose_name="10.1 Трудозатраты, дн. (на устранение замечания) (План)",
            ),
        ),
        migrations.AlterField(
            model_name="reestr",
            name="root_cause_list",
            field=models.TextField(verbose_name="15. Коренная причина"),
        ),
        migrations.AlterField(
            model_name="reestr",
            name="total_importance",
            field=models.TextField(verbose_name="14. Значимость замечания"),
        ),
    ]