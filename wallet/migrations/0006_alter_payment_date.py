# Generated by Django 4.2.6 on 2023-10-26 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_alter_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.CharField(max_length=20, verbose_name='Дата оплаты'),
        ),
    ]
