# Generated by Django 5.0.3 on 2024-09-11 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_proxy_city_proxy_country_proxy_ip_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigns',
            name='continent',
        ),
        migrations.AddField(
            model_name='campaigns',
            name='country',
            field=models.CharField(blank=True, choices=[('United Kingdom', 'United Kingdom'), ('New Zealand', 'New Zealand'), ('United States', 'United States')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='campaigns',
            name='time_zone',
            field=models.CharField(max_length=100),
        ),
    ]
