# Generated by Django 4.2.5 on 2024-07-06 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_campaigns_time_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaigns',
            name='repetition_done',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
