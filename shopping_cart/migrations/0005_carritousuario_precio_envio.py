# Generated by Django 4.1.2 on 2023-05-24 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0004_alter_detallecarritoproducto_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='carritousuario',
            name='precio_envio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
