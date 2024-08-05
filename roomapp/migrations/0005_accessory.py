# Generated by Django 5.0.7 on 2024-08-05 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomapp', '0004_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='accessory_images/')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessories', to='roomapp.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessories', to='roomapp.user')),
            ],
        ),
    ]
