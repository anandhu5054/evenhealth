# Generated by Django 4.1.5 on 2023-02-21 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0009_doctorprofile_consultation_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='booked_tokens',
            field=models.IntegerField(default=0),
        ),
    ]
