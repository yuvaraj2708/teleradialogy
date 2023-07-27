# Generated by Django 4.2 on 2023-07-27 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_device_registered', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ekon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uhid', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('patient_name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('age', models.CharField(max_length=255)),
                ('email_id', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=255)),
                ('accession_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='patientcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RefDr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DoctorCode', models.CharField(max_length=100)),
                ('DoctorName', models.CharField(max_length=100)),
                ('Qualification', models.CharField(max_length=100)),
                ('Specialisation', models.CharField(max_length=100)),
                ('Address', models.CharField(max_length=100)),
                ('PINCode', models.CharField(max_length=100)),
                ('Mobile', models.CharField(max_length=100)),
                ('EmailID', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testid', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('specimen_type', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('report_format', models.CharField(max_length=100)),
                ('reporting_rate', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_category', models.CharField(max_length=255)),
                ('ref_dr', models.CharField(max_length=255)),
                ('visit_id', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ekonapp.ekon')),
                ('selected_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ekonapp.test')),
            ],
        ),
        migrations.CreateModel(
            name='Scansummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jpgfile', models.ImageField(upload_to='scans/')),
                ('scandetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ekonapp.visit')),
            ],
        ),
        migrations.CreateModel(
            name='Devicecheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50)),
                ('client_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('pin_code', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50)),
                ('client_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('pin_code', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('is_registered', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
