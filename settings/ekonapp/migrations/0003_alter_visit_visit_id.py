# Generated by Django 4.2 on 2023-07-20 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekonapp', '0002_alter_test_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='visit_id',
            field=models.CharField(max_length=100),
        ),
    ]