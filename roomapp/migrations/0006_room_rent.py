# Generated by Django 5.0.7 on 2024-08-05 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomapp', '0005_accessory'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='rent',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
    ]
