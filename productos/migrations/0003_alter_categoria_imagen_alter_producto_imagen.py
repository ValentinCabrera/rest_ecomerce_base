# Generated by Django 4.1.2 on 2023-08-17 04:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("productos", "0002_alter_categoria_imagen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categoria",
            name="imagen",
            field=models.ImageField(upload_to="productos/static/categorias"),
        ),
        migrations.AlterField(
            model_name="producto",
            name="imagen",
            field=models.ImageField(upload_to="productos/static/productos"),
        ),
    ]
