# Generated by Django 4.1.5 on 2023-02-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0010_alter_slot_booked_tokens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='booked_tokens',
            field=models.IntegerField(default=1),
        ),
    ]
