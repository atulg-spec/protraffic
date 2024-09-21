# Generated by Django 5.1.1 on 2024-09-21 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0057_alter_campaignpage_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaigns',
            name='main_proxy',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='campaigns',
            name='session_string_length',
            field=models.PositiveIntegerField(default=12),
        ),
    ]
