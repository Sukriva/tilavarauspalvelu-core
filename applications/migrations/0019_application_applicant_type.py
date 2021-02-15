# Generated by Django 3.0.10 on 2021-02-15 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0018_organisation_core_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='applicant_type',
            field=models.CharField(choices=[('individual', 'Individual'), ('association', 'Association'), ('community', 'Community'), ('company', 'Company')], default='individual', max_length=64, verbose_name='Applicant type'),
            preserve_default=False,
        ),
    ]