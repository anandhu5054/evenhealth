# Generated by Django 4.1.5 on 2023-02-12 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0005_doctorprofile_is_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorprofile',
            name='is_approved',
        ),
    ]
