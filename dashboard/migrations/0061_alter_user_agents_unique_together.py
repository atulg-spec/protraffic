# Generated by Django 5.1.1 on 2024-09-26 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0060_alter_user_agents_options_user_agents_webgl_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user_agents',
            unique_together=set(),
        ),
    ]
