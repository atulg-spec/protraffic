# Generated by Django 5.0.3 on 2024-08-30 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_pagebehaviour_remove_campaigns_scroll_duration_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaigns',
            name='direct_traffic',
            field=models.BooleanField(default=False),
        ),
    ]
