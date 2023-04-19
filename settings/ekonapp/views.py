from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
import uuid
from django.http import HttpResponse
from .utils import generate_uhid
from django.db.models import Q

# Create your views here.
User = get_user_model()

@login_required
def patientregistration(request):
    if 'uhid' not in request.session:
        request.session['uhid'] = generate_uhid()
    
    if request.method == 'POST':
        # Extract form data from request.POST dictionary
        title = request.POST.get('title')
        gender = request.POST.get('gender')
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        email_id = request.POST.get('email_id')
        contact_number = request.POST.get('contact_number')
        patient_history = request.POST.get('patient_history')
        status = request.POST.get('status')
        date = request.POST.get('date')
        # Create a new Patient object
        patient = ekon(uhid=request.session['uhid'], title=title, gender=gender, patient_name=patient_name, dob=dob,
                          age=age, email_id=email_id, contact_number=contact_number, patient_history=patient_history,
                          status=status,date=date)
        # Save the Patient object to the database
        patient.save()
        # Generate a new uhid for the next patient registration
        request.session['uhid'] = generate_uhid()

    return render(request, 'patient-registration.html', {'uhid': request.session['uhid']})


  




@login_required
def addvisit(request):
    
    return render(request,'add-visit.html')


@login_required
def registrationsummary(request):
    patients = ekon.objects.all()
    
    if request.method == 'POST':
        date = request.POST.get('date')
        patient_name = request.POST.get('patient_name')
        status = request.POST.get('status')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        
        # Filter by patient name
        if patient_name:
            patients = patients.filter(Q(patient_name__icontains=patient_name) | Q(uhid__icontains=patient_name))
        
        # Filter by status
        if status:
            patients = patients.filter(status=status)
        
        # Filter by date range
        if from_date and to_date:
            patients = patients.filter(date__range=[from_date, to_date])
        
        
        context = {'patients': patients}
        
    else:
        context = {
            'patients': patients
        }
        
    return render(request, 'registration-summary.html', context)


@login_required
def visitsummary(request):
    return render(request,'visit-summary.html')


@login_required
def register_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        client_name = request.POST.get('client_name')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        
        # Create and save the device
        device = Device(
            device_id=device_id,
            client_name=client_name,
            address=address,
            pin_code=pin_code,
            mobile_number=mobile_number,
            email=email,
        )
        device.save()
        
    return render(request, 'registerdevice.html')