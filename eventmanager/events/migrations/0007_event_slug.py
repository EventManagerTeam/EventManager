# Generated by Django 2.1.2 on 2018-11-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20181108_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
