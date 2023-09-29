# Generated by Django 4.1.2 on 2023-09-28 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("productos", "0010_catalogo_varianteproducto_itemcatalogo"),
        ("pedidos", "0009_alter_itempedido_producto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itempedido",
            name="pedido",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="pedidos.pedido",
            ),
        ),
        migrations.AlterField(
            model_name="itempedido",
            name="producto",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="productos.producto"
            ),
        ),
    ]
