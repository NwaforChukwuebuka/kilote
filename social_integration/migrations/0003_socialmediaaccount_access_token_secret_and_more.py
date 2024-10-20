# Generated by Django 5.1.1 on 2024-10-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_integration', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmediaaccount',
            name='access_token_secret',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='socialmediaaccount',
            name='screen_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
