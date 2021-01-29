# Generated by Django 3.0.10 on 2021-01-29 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0009_add_coordinates_and_unit_to_location'),
        ('reservation_units', '0007_reservation_units_modeltranslation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationunit',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spaces.Unit', verbose_name='Unit'),
        ),
    ]
