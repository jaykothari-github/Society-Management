# Generated by Django 4.0 on 2021-12-26 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SecApp', '0003_emergency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emergency',
            old_name='number',
            new_name='mobile',
        ),
    ]
