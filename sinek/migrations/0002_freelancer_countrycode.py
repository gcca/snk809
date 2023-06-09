# Generated by Django 4.0.3 on 2022-05-03 19:36

from django.db import migrations, models

from sinek.domain.model.freelancer import Phone


class Migration(migrations.Migration):

  dependencies = [
    ('sinek', '0001_initial'),
  ]

  operations = [
    migrations.AddField(
      model_name='freelancer',
      name='countryCode',
      field=models.IntegerField(default=Phone.CountryCode.PER.value),
      preserve_default=False,
    ),
  ]
