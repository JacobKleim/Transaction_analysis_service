# Generated by Django 5.2.3 on 2025-06-18 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaction_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('Food', 'Еда'), ('Transport', 'Транспорт'), ('Entertainment', 'Развлечения'), ('Utilities', 'Коммунальные услуги'), ('Other', 'Другое')], default='Other', max_length=20),
        ),
    ]
