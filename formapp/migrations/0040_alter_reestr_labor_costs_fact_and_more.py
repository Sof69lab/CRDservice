# Generated by Django 4.1 on 2024-03-06 11:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0039_reestr_reestrid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reestr",
            name="labor_costs_fact",
            field=models.FloatField(
                blank=True,
                null=True,
                verbose_name="10.2. Трудозатраты, дн. (на устранение замечания) (Факт)",
            ),
        ),
        migrations.AlterField(
            model_name="reestr",
            name="link_tech_name",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="12. Ссылка  в  технической документации",
            ),
        ),
    ]
