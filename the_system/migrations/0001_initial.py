# Generated by Django 3.2.13 on 2022-04-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemConfig',
            fields=[
                ('config', models.CharField(choices=[('APP_NAME', 'APPLICATION NAME'), ('SITE_HEADER', 'ADMIN SITE HEADER'), ('SITE_TITLE', 'ADMIN SITE TITLE'), ('INDEX_TITLE', 'ADMIN SITE INDEX TITLE'), ('POWERED_BY', 'POWERED BY WEBSITE'), ('BATCH_TRANSATION_POSTING', 'BATCH TRANSATION POSTING')], max_length=25, primary_key=True, serialize=False, verbose_name='Configuration Name')),
                ('value', models.CharField(max_length=100, verbose_name='Value')),
            ],
            options={
                'verbose_name': 'System Configuration',
            },
        ),
    ]
