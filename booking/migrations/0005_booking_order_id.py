# Generated by Django 4.1.5 on 2023-02-24 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_rename_token_booking_token_alter_booking_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='order_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
