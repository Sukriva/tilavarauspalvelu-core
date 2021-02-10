# Generated by Django 3.0.10 on 2021-02-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0012_district_translations'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('units', models.ManyToManyField(related_name='unit_groups', to='spaces.Unit')),
            ],
        ),
    ]
