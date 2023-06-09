# Generated by Django 4.1.3 on 2022-12-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onboard", "0005_onboard_show_resume_alter_onboard_resume"),
    ]

    operations = [
        migrations.AddField(
            model_name="googleform",
            name="view_link",
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name="onboard",
            name="google_forms",
            field=models.ManyToManyField(to="onboard.googleform"),
        ),
    ]
