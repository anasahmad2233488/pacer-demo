# Generated by Django 4.1.4 on 2022-12-29 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='score_d',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
