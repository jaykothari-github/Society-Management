# Generated by Django 4.0 on 2022-01-19 05:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SecApp', '0007_secuser_setting'),
        ('MemberApp', '0008_complain'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='solve_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SecApp.secuser'),
        ),
        migrations.AlterField(
            model_name='complain',
            name='solved_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 19, 11, 16, 30, 619818)),
        ),
    ]
