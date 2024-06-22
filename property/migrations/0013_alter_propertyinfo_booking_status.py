# Generated by Django 5.0.1 on 2024-04-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0012_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyinfo',
            name='Booking_Status',
            field=models.CharField(choices=[('Listing', 'Listing'), ('Booked', 'Booked'), ('Reserved', 'Reserved')], default='Listing', max_length=20),
        ),
    ]
