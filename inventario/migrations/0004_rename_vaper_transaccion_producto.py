# Generated by Django 5.1.7 on 2025-03-27 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_rename_producto_transaccion_vaper'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaccion',
            old_name='vaper',
            new_name='producto',
        ),
    ]
