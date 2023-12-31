# Generated by Django 4.1.2 on 2023-08-18 00:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("productos", "0003_alter_categoria_imagen_alter_producto_imagen"),
    ]

    operations = [
        migrations.RenameField(
            model_name="producto",
            old_name="categorias",
            new_name="categoria",
        ),
        migrations.AlterField(
            model_name="categoria",
            name="nombre",
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
