# Generated by Django 2.1.2 on 2018-12-04 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_invite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invite',
            options={'verbose_name': 'Invite', 'verbose_name_plural': 'Invites'},
        ),
    ]
