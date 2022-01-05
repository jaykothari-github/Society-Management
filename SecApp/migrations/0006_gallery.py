# Generated by Django 4.0 on 2022-01-03 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SecApp', '0005_alter_secuser_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.FileField(upload_to='Gallery')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecApp.secuser')),
            ],
        ),
    ]