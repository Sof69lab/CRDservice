# Generated by Django 4.1 on 2023-12-01 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0010_alter_reestr_answer_date_fact_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reestr",
            name="remark_v",
            field=models.IntegerField(verbose_name="1.2. Версия замечания"),
        ),
    ]