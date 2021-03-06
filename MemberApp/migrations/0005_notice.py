# Generated by Django 4.0 on 2021-12-29 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SecApp', '0005_alter_secuser_pic'),
        ('MemberApp', '0004_member_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('des', models.TextField()),
                ('pic', models.FileField(blank=True, null=True, upload_to='Notice')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MemberApp.member')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecApp.secuser')),
            ],
        ),
    ]
