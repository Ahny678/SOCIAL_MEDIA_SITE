# Generated by Django 5.0.7 on 2024-10-19 18:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clone', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videopost',
            name='post_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
