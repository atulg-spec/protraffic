# Generated by Django 4.2.5 on 2024-07-12 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_useragentsfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaigns',
            name='extension_path',
            field=models.CharField(default='C:/Users/Administrator/Desktop/WebRTC-Leak-Prevent', max_length=100),
        ),
    ]
