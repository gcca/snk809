# Generated by Django 4.0.3 on 2022-06-03 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

  dependencies = [
    ('sinek', '0002_freelancer_countrycode'),
  ]

  operations = [
    migrations.AddField(
      model_name='upload',
      name='googleId',
      field=models.CharField(max_length=256, null=True),
    ),
    migrations.AlterField(
      model_name='upload',
      name='binary',
      field=models.BinaryField(null=True),
    ),
  ]