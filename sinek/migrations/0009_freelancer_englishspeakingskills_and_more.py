# Generated by Django 4.0.3 on 2022-09-26 17:19

from django.db import migrations, models
import django.db.models.deletion
import sinek.domain.model.freelancer


class Migration(migrations.Migration):

    dependencies = [
        ('sinek', '0008_freelancer_isonboarded'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='englishSpeakingSkills',
            field=models.IntegerField(choices=[(0, 'Nosettled'), (1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced'), (4, 'Proficient')], default=sinek.domain.model.freelancer.EnglishProficiency.EnglishSkill['NOSETTLED']),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='englishWritingSkills',
            field=models.IntegerField(choices=[(0, 'Nosettled'), (1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced'), (4, 'Proficient')], default=sinek.domain.model.freelancer.EnglishProficiency.EnglishSkill['NOSETTLED']),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='interviewAvailability',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='jobSwitchTime',
            field=models.IntegerField(choices=[(0, 'Nosettled'), (1, 'Bw 1M 2M'), (2, 'Bw 3M 6M'), (3, 'Bw 6M 12M'), (4, 'Gt 12M')], default=sinek.domain.model.freelancer.AcceptanceAvailability.JobSwitchTime['NOSETTLED']),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='maxIncome',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='wouldChangeCity',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='wouldChangeCountry',
            field=models.BooleanField(null=True),
        ),
        migrations.CreateModel(
            name='FreelancerWorklifeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worklifePreferences', to='sinek.freelancer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FreelancerRoleTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roleInterests', to='sinek.freelancer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FreelancerJobTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobPreferences', to='sinek.freelancer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
