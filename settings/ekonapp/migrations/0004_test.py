# Generated by Django 3.2.18 on 2023-04-20 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekonapp', '0003_device_is_registered'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=100, unique=True)),
                ('specimen_type', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('microbiology', 'Microbiology'), ('pathology', 'Pathology'), ('radiology', 'Radiology')], max_length=100)),
                ('report_format', models.CharField(max_length=100)),
                ('reporting_rate', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
