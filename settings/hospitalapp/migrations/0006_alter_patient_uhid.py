# Generated by Django 3.2.18 on 2023-04-18 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitalapp', '0005_alter_patient_uhid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='uhid',
            field=models.CharField(max_length=255),
        ),
    ]
