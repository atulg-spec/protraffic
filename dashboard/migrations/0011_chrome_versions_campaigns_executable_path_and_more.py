# Generated by Django 4.2.5 on 2024-07-07 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_campaigns_repetition_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chrome_versions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Chrome Version',
                'verbose_name_plural': 'Chrome Versions',
                'unique_together': {('version',)},
            },
        ),
        migrations.AddField(
            model_name='campaigns',
            name='executable_path',
            field=models.CharField(default='C:/Program Files/Google/Chrome/Application/chrome.exe', max_length=100),
        ),
        migrations.AddField(
            model_name='campaigns',
            name='user_Data_Dir',
            field=models.CharField(default='C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default', max_length=100),
        ),
        migrations.AddField(
            model_name='campaigns',
            name='user_agents',
            field=models.ManyToManyField(to='dashboard.chrome_versions'),
        ),
        migrations.CreateModel(
            name='User_agents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_agent', models.CharField(default='', max_length=200)),
                ('chrome_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.chrome_versions')),
            ],
            options={
                'verbose_name': 'User Agent',
                'verbose_name_plural': 'User Agents',
                'unique_together': {('chrome_version', 'user_agent')},
            },
        ),
    ]
