# Generated by Django 4.1.2 on 2023-08-21 01:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0011_alter_token_asset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="asset",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 8, 22, 1, 16, 57, 732687)
            ),
        ),
    ]