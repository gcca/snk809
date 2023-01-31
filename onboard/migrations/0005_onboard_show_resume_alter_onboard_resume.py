# Generated by Django 4.0.3 on 2022-12-21 23:48

from django.db import migrations, models

import onboard.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "onboard",
            "0004_rename_agilitylearninginput_"
            "complexinstructionsinput_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="onboard",
            name="show_resume",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="onboard",
            name="resume",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=onboard.models.ResumeDirectoryPath,
            ),
        ),
    ]