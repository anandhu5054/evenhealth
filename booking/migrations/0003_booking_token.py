# Generated by Django 4.1.5 on 2023-02-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_remove_booking_date_booked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='Token',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]