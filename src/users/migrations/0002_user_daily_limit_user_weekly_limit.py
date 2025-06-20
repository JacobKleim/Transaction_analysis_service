# Generated by Django 5.2.3 on 2025-06-18 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='daily_limit',
            field=models.FloatField(default=5000, verbose_name='Дневной лимит трат'),
        ),
        migrations.AddField(
            model_name='user',
            name='weekly_limit',
            field=models.FloatField(default=35000, verbose_name='Недельный лимит трат'),
        ),
    ]
