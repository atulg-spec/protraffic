# Generated by Django 4.2.7 on 2024-09-29 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0063_campaigns_profiles_tag_campaigns_use_login_profiles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='youtube_subscribe',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tasks',
            name='youtube_views',
            field=models.BooleanField(default=False),
        ),
    ]
