# Generated by Django 5.1.4 on 2025-04-04 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
