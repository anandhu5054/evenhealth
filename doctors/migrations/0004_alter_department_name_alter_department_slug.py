# Generated by Django 4.1.5 on 2023-02-11 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_department_slug_alter_department_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
