# Generated by Django 5.0.1 on 2024-04-01 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='before_service_fee',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='service_fee',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.FloatField(),
        ),
    ]
