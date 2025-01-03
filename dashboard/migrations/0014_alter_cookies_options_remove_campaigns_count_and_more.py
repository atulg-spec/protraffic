# Generated by Django 4.2.5 on 2024-07-12 07:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0013_campaigns_cookies_file_cookies'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cookies',
            options={'verbose_name': 'Cookie', 'verbose_name_plural': 'Cookies'},
        ),
        migrations.RemoveField(
            model_name='campaigns',
            name='count',
        ),
        migrations.RemoveField(
            model_name='campaigns',
            name='from_time',
        ),
        migrations.RemoveField(
            model_name='campaigns',
            name='repetition_count',
        ),
        migrations.RemoveField(
            model_name='campaigns',
            name='repetition_done',
        ),
        migrations.RemoveField(
            model_name='campaigns',
            name='to_time',
        ),
        migrations.RemoveField(
            model_name='campaigns',
            name='user',
        ),
        migrations.AddField(
            model_name='tasks',
            name='count',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='tasks',
            name='repetition_count',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='tasks',
            name='repetition_done',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='tasks',
            name='user',
        ),
        migrations.AddField(
            model_name='tasks',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
