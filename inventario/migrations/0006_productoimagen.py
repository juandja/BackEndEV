# Generated by Django 5.1.7 on 2025-04-01 04:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_producto_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoImagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='productos/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='inventario.producto')),
            ],
        ),
    ]
