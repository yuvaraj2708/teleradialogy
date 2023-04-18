from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
import uuid
from django.http import HttpResponse

# Create your views here.
User = get_user_model()

@login_required
def patientregistration(request):
    if request.method == 'POST':
        # Extract form data from request.POST dictionary
        uhid = request.POST.get('uhid')
        title = request.POST.get('title')
        gender = request.POST.get('gender')
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        email_id = request.POST.get('email_id')
        contact_number = request.POST.get('contact_number')
        patient_history = request.POST.get('patient_history')
        status = request.POST.get('status')

        # Create a new Patient object
        patient = Patient(uhid=uhid, title=title, gender=gender, patient_name=patient_name, dob=dob,
                          age=age, email_id=email_id, contact_number=contact_number, patient_history=patient_history,
                          status=status)
        # Save the Patient object to the database
        patient.save()
    return render(request, 'patient-registration.html') 


@login_required
def addvisit(request):
    
    return render(request,'add-visit.html')