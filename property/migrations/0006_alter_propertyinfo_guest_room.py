# Generated by Django 5.0.1 on 2024-02-21 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_alter_propertyinfo_property_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyinfo',
            name='guest_room',
            field=models.CharField(blank=True, choices=[('entire_place', 'Entire Place'), ('a_room', 'A Room'), ('shared_room', 'Shared Room')], default=None, max_length=20, null=True),
        ),
    ]
