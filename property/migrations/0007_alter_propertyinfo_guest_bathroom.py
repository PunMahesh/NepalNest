# Generated by Django 5.0.1 on 2024-02-21 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_alter_propertyinfo_guest_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyinfo',
            name='guest_bathroom',
            field=models.CharField(blank=True, choices=[('private_bathroom', 'Private and Attached'), ('dedicated_bathroom', 'Dedicated'), ('shared_bathroom', 'Shared')], default=None, max_length=20, null=True),
        ),
    ]
