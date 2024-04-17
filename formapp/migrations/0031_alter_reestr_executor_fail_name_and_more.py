# Generated by Django 4.1 on 2024-01-25 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("formapp", "0030_alter_reestr_executor_fail_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reestr",
            name="executor_fail_name",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="executFail_set",
                to=settings.AUTH_USER_MODEL,
                verbose_name="6. Исполнитель, допустивший замечание",
            ),
        ),
        migrations.AlterField(
            model_name="reestr",
            name="executor_name",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="execut_set",
                to=settings.AUTH_USER_MODEL,
                verbose_name="6.1. Исполнитель, ответственный за устранение замечания",
            ),
        ),
    ]
