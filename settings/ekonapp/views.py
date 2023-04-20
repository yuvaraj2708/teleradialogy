from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
import uuid
from django.http import HttpResponse
from .utils import generate_uhid
from django.db.models import Q
from .utils import require_purchase
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponseNotFound
from django.contrib import messages

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
    if request.session.get('registered'):
        # User has already registered, redirect to registration summary
        return redirect('registrationsummary')
    
    if request.method == 'POST':
        # Handle form submission
        device_id = request.POST['device_id']
        client_name = request.POST['client_name']
        address = request.POST['address']
        pin_code = request.POST['pin_code']
        mobile_number = request.POST['mobile_number']
        email = request.POST['email']
        
        # Check if device has already been registered
        try:
            device = Device.objects.get(device_id=device_id)
            if device.is_registered:
                # device has already been registered, show error message
                return render(request, 'error.html', {'message': 'Device has already been registered.'})
        except Device.DoesNotExist:
            pass
        
        # Create a new device object
        device = Device(device_id=device_id, client_name=client_name, address=address, pin_code=pin_code, mobile_number=mobile_number, email=email)
        device.save()
        
        # Set session variable to indicate that user has registered
        request.session['registered'] = True
        
        # Redirect to registration summary
        return redirect('registrationsummary')
    else:
        # Render registration form
        return render(request, 'registerdevice.html')


def addtest(request):
    if request.method == 'POST':
        today = datetime.today().strftime('%Y-%m-%d')
        date = request.POST.get('date', today)
        name = request.POST.get('name')
        specimen_type = request.POST.get('specimen_type')
        department = request.POST.get('department')
        report_format = request.POST.get('report_format')
        reporting_rate = request.POST.get('reporting_rate')
        
        
        testmaster = Test(date=date, name=name, specimen_type=specimen_type, department=department, report_format=report_format, reporting_rate=reporting_rate)
        testmaster.save()
        
            
    return render(request,'addtest.html')
    
def testmaster(request):
    testmasters = Test.objects.all()
    
    context = {
        'testmasters':testmasters,
    }
    return render(request,'tests-master.html',context)


# def addvisit(request, id):
#     patient = ekon.objects.get(id=id)

#     if request.method == 'POST':
#         uhid  = request.POST.get('uhid')
#         title = request.POST.get('title')
#         gender = request.POST.get('gender')
#         patient_name = request.POST.get('patient_name')
#         dob = request.POST.get('dob')
#         age = request.POST.get('age')
#         email_id = request.POST.get('email_id')
#         contact_number = request.POST.get('contact_number')
#         patient_history = request.POST.get('patient_history')
#         status = request.POST.get('status')
#         date = request.POST.get('date')

#         # Update the patient object with form data
#         patient.uhid=uhid
#         patient.title=title
#         patient.gender=gender
#         patient.patient_name=patient_name
#         patient.dob=dob
#         patient.age=age
#         patient.email_id=email_id
#         patient.contact_number=contact_number
#         patient.patient_history=patient_history
#         patient.status=status
#         patient.date=date
#         patient.save()
        
        
#         messages.error(request, 'A test with that name already exists.')
#         return redirect('registrationsummary')
         
        
#     return render(request, 'add-visit.html')


def addvisit(request, id):
    patient = ekon.objects.get(id=id)
    context = {'patient': patient}
    return render(request, 'add-visit.html', context)
