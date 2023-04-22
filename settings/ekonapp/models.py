from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth import get_user_model
import uuid
from django.db.models.signals import pre_delete


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, name, password, **extra_fields):
        if not name:
            raise ValueError('The Name field must be set')

        name = self.normalize_email(name)
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_device_registered = models.BooleanField(default=False)  # new field
    
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.name
  
    def has_module_perms(self, app_label):
        return True


User = get_user_model()

class Device(models.Model):
    device_id = models.CharField(max_length=50)
    client_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    is_authenticated = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)  # new field

    def __str__(self):
        return f"{self.device_id} ({self.client_name})"

    
    
    
class Test(models.Model):
    testid = models.CharField(max_length=255)
    date =  models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    specimen_type = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=[('microbiology', 'Microbiology'), ('pathology', 'Pathology'), ('radiology', 'Radiology')])
    report_format = models.CharField(max_length=100)
    reporting_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class RefDr(models.Model):
    DoctorCode  = models.CharField(max_length=100)
    DoctorName = models.CharField(max_length=100)
    Qualification= models.CharField(max_length=100)
    Specialisation= models.CharField(max_length=100)
    Address= models.CharField(max_length=100)
    PINCode = models.CharField(max_length=100)
    Mobile= models.CharField(max_length=100)
    EmailID= models.CharField(max_length=100)
    date =  models.DateField(auto_now_add=True)
    
    
    
class ekon(models.Model):
    uhid = models.CharField(max_length=255)
    Mr = 'Mr'
    Miss = 'Miss'
    STATUS_CHOICES = [
        (Mr, 'Mr'),
        (Miss, 'Miss'),
    ]
    title = models.CharField(max_length=255)
    male = 'male'
    female = 'female'
    STATUS_CHOICES = [
        (male, 'male'),
        (female, 'female'),
    ]
    gender = models.CharField(max_length=255)
    patient_name = models.CharField(max_length=255)
    dob = models.DateField()
    age = models.IntegerField()
    email_id = models.EmailField()
    contact_number = models.CharField(max_length=255)
    patient_history = models.TextField()
    date =  models.DateField(auto_now_add=True)
    
    Active = 'Active'
    Inactive = 'Inactive'
    STATUS_CHOICES = [
        (Active, 'Active'),
        (Inactive, 'Inactive'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
  
    

import uuid

class Visit(models.Model):
    patient = models.ForeignKey(ekon, on_delete=models.CASCADE)
    patient_category = models.CharField(max_length=255)
    ref_dr =  models.CharField(max_length=255)
    selected_test = models.CharField(max_length=255)
    visit_id = models.CharField(max_length=7, unique=True, editable=False)
    date =  models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.visit_id = 'V' + str(uuid.uuid4().int)[:5]
        super(Visit, self).save(*args, **kwargs)

    
    
class patientcategory(models.Model):
    category = models.CharField(max_length = 255)