# Generated by Django 4.1.5 on 2023-02-03 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=30, null=True)),
                ('emergency_contact_relationship', models.CharField(blank=True, max_length=30, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+ve'), ('B+', 'B+ve'), ('AB+', 'AB+ve'), ('O+', 'O+ve'), ('A-', 'A-ve'), ('B-', 'B-ve'), ('AB-', 'AB-ve'), ('O-', 'O-ve')], max_length=3, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]