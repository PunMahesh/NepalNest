# Generated by Django 5.0.1 on 2024-04-17 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_alter_propertyinfo_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyinfo',
            name='Booking_Status',
            field=models.CharField(blank=True, choices=[('Listing', 'Listing'), ('Booked', 'Booked'), ('Reserved', 'Reserved')], default=None, max_length=20, null=True),
        ),
    ]
