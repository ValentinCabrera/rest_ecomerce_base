# Generated by Django 4.1.2 on 2023-08-17 04:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0002_alter_token_asset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="asset",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 8, 18, 4, 16, 25, 441098)
            ),
        ),
    ]