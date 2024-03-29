# Generated by Django 5.0.1 on 2024-03-07 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyinfo',
            name='images',
        ),
        migrations.AddField(
            model_name='propertyinfo',
            name='PropertyPhoto',
            field=models.ImageField(blank=True, upload_to='Photo'),
        ),
        migrations.AlterField(
            model_name='ammenities',
            name='name',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='extra_items',
            name='name',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='other_ammenities',
            name='name',
            field=models.CharField(max_length=225, unique=True),
        ),
        migrations.AlterField(
            model_name='safety_items',
            name='name',
            field=models.CharField(max_length=225, unique=True),
        ),
    ]
