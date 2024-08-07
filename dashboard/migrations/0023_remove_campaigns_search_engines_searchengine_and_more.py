# Generated by Django 4.2.5 on 2024-07-13 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_tasks_facebook_campaign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigns',
            name='search_engines',
        ),
        migrations.CreateModel(
            name='SearchEngine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engine', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Search Engine',
                'verbose_name_plural': 'Search Engines',
                'unique_together': {('engine',)},
            },
        ),
        migrations.AddField(
            model_name='campaigns',
            name='search_engines',
            field=models.ManyToManyField(to='dashboard.searchengine'),
        ),
    ]
