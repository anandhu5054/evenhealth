# Generated by Django 4.1.5 on 2023-02-18 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0007_slot_number_of_patients_alter_qualification_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='booked_tokens',
            field=models.TextField(default='[]'),
        ),
    ]
