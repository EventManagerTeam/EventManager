# Generated by Django 2.1.2 on 2018-11-02 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20181102_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='eventmanager/media/pictures_models/'),
        ),
    ]
