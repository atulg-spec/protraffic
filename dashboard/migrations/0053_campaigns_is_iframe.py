# Generated by Django 5.0.3 on 2024-09-13 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0052_alter_campaigns_time_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaigns',
            name='is_iframe',
            field=models.BooleanField(default=False),
        ),
    ]
