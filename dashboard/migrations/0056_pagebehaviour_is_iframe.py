# Generated by Django 5.0.3 on 2024-09-13 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0055_alter_pagebehaviour_click_selector'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagebehaviour',
            name='is_iframe',
            field=models.BooleanField(default=False),
        ),
    ]