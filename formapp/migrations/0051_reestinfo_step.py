# Generated by Django 4.1 on 2024-04-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formapp", "0050_files_belong_to_alter_files_file_alter_files2_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="reestinfo",
            name="step",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
