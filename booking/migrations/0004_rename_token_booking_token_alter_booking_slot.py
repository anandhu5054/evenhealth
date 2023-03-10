# Generated by Django 4.1.5 on 2023-02-23 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0012_alter_doctorprofile_user'),
        ('booking', '0003_booking_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='Token',
            new_name='token',
        ),
        migrations.AlterField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='doctors.slot'),
        ),
    ]
