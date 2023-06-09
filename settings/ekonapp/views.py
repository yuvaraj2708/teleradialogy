from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
import uuid
from django.http import HttpResponse
from .utils import generate_uhid,generate_testuhid,generate_Doctoruhid,generate_accession_number
from django.db.models import Q
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm
from django.contrib.auth import login,authenticate
from .decorators import device_required
import os
import pydicom
from PIL import Image
import numpy as np
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from .serializers import *
from rest_framework import viewsets
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.http import HttpResponse
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4

# Create your views here.
User = get_user_model()

@login_required
@device_required
def patientregistration(request):
    if 'uhid' not in request.session:
        request.session['uhid'] = generate_uhid()

    if 'accession_number' not in request.session:
        request.session['accession_number'] = generate_accession_number()

    if request.method == 'POST':
        # Extract form data from request.POST dictionary
        title = request.POST.get('title')
        gender = request.POST.get('gender')
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        email_id = request.POST.get('email_id')
        contact_number = request.POST.get('contact_number')
        # patient_history = request.POST.get('patient_history')
        status = request.POST.get('status')
        date = request.POST.get('date')

        # Generate a new accession number
        accession_number = generate_accession_number()

        # Create a new Patient object
        patient = ekon(
            uhid=request.session['uhid'],
            title=title,
            gender=gender,
            patient_name=patient_name,
            dob=dob,
            age=age,
            email_id=email_id,
            contact_number=contact_number,
            status=status,
            date=date,
            accession_number=accession_number
        )

        # Save the Patient object to the database
        patient.save()

        # Generate a new uhid for the next patient registration
        request.session['uhid'] = generate_uhid()

        # Create a folder for barcode images if it doesn't exist
       
        # Update the stored accession number and barcode path in the session
        request.session['accession_number'] = accession_number
       
        return redirect('registrationsummary')

    return render(request, 'patient-registration.html', {'uhid': request.session['uhid']})






@login_required
@device_required
def registrationsummary(request):
    patients = ekon.objects.all()
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        status = request.POST.get('status')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        contact_number = request.POST.get('contact_number')
        
        # Filter by patient name
        if patient_name:
            patients = patients.filter(Q(patient_name__icontains=patient_name) | Q(uhid__icontains=patient_name))
        
        # Filter by status
        if status:
            patients = patients.filter(status=status)
        
        # Filter by date range
        if from_date and to_date:
            patients = patients.filter(date__range=[from_date, to_date])
        
        if contact_number:
            patients = patients.filter(contact_number__icontains=contact_number)
        
        context = {'patients': patients,}
        
    else:
        context = {
            'patients': patients
        }
        
    return render(request, 'registration-summary.html', context)


@login_required
def registerlogin(request):
    if request.user.is_authenticated:
        user = request.user
        # Check if user has a registered device
        if Device.objects.filter(user=user, is_registered=True).exists():
            # User has a registered device, show the registration summary page
            return render(request, 'registration-summary.html')
        else:
            # User doesn't have a registered device, redirect to the device registration page
            return redirect('register_device')
    # Redirect to device register if user is not authenticated
    return redirect('register_device')




@login_required
def register_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        client_name = request.POST.get('client_name')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        
        if not device_id or not client_name or not address or not pin_code or not mobile_number or not email:
            # Render registration form with an error message
            return render(request, 'registerdevice.html', {'error': 'Please fill in all the required fields.'})
        
        # Check if device is already registered
        try:
            device = Device.objects.get(device_id=device_id)
            if device.is_registered:
                # Device is already registered, render the registration form with an error message
                return render(request, 'registerdevice.html', {'error': 'Device is already registered.'})
        except Device.DoesNotExist:
            # Device is not registered, create a new Device object
            device = Device(device_id=device_id)

        # Set the other fields and save the device object
        device.client_name = client_name
        device.address = address
        device.pin_code = pin_code
        device.mobile_number = mobile_number
        device.email = email
        device.is_registered = True
        device.user = request.user
        device.save()

        # Set the is_device_registered flag on the user object
        user = request.user
        user.is_device_registered = True
        user.save()

        # Redirect to the registration summary page
        return redirect('registrationsummary')

    # Render the registration form if the request method is GET
    return render(request, 'registerdevice.html')






@login_required
@device_required
def addtest(request):
    if 'testid' not in request.session:
        request.session['testid'] = generate_testuhid()
    if request.method == 'POST':
        name = request.POST.get('name')
        specimen_type = request.POST.get('specimen_type')
        department = request.POST.get('department')
        report_format = request.POST.get('report_format')
        reporting_rate = request.POST.get('reporting_rate')
        
        
        testmaster = Test(testid=request.session['testid'], name=name, specimen_type=specimen_type, department=department, report_format=report_format, reporting_rate=reporting_rate)
        testmaster.save()
        
        request.session['testid'] = generate_testuhid()
            
    return render(request,'addtest.html', {'testid': request.session['testid']})


@login_required
@device_required
def testmaster(request):
    testmasters = Test.objects.all()
    departments = Test.objects.values('department').distinct()

    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        
        # Filter by test name or code
        if name:
            testmasters = testmasters.filter(models.Q(name__icontains=name) | models.Q(testid__icontains=name))
        
        # Filter by department
        if department:
            testmasters = testmasters.filter(department__icontains=department)
        
    context = {
        'testmasters': testmasters,
        'departments': departments,
    }
        
    return render(request, 'tests-master.html', context)
 

@login_required
@device_required
def addvisit(request, id):
    refdrs = RefDr.objects.all() 
    patient = ekon.objects.get(id=id)
    select_test = Test.objects.all()
    patientscategory = patientcategory.objects.all()
    if request.method == 'POST':
        # Extract form data from request.POST dictionary
        patient_category = request.POST.get('patient_category')
        ref_dr = request.POST.get('ref_dr')
        selected_test = request.POST.get('selected_test')
        # Create a new Visit object
        visit = Visit(patient=patient, patient_category=patient_category, ref_dr=ref_dr, selected_test=selected_test)
        # Save the Visit object to the database
        visit.save()
        # Redirect to the page where you want to display both models
        return redirect('visitsummary')
    context = {'patient': patient,
               'refdrs': refdrs,
               'select_test':select_test,
               'patientscategory':patientscategory,
               }
    return render(request, 'add-visit.html', context)


    
    
@login_required
@device_required
def visitsummary(request):
    visits = Visit.objects.all()
    if request.method == 'POST':
        visit_id = request.POST.get('visit_id')
        status = request.POST.get('status')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        # Filter by visit id
        if visit_id:
            visits = visits.filter(visit_id__icontains=visit_id)
        
        # Filter by status
        if status:
            visits = visits.filter(status=status)
        
        # Filter by date range
        if from_date and to_date:
            visits = visits.filter(date__range=[from_date, to_date])
        
        
        context = {'visits': visits, 'from_date': from_date, 'to_date': to_date}
        
    else:
        context = {'visits': visits}
        
    return render(request, 'visit-summary.html', context)


@device_required
def deleteregistersummary(request, id):
    patient = ekon.objects.get(id=id)
    
    patient.delete()
    return redirect('registrationsummary')
@device_required
def deletevisit(request, id):
    patient = Visit.objects.get(id=id)
    
    patient.delete()
    return redirect('visitsummary')
@device_required
def delete(request, id):
    patient = RefDr.objects.get(id=id)
    
    patient.delete()
    return redirect('refdrmaster')
@device_required
def deletetest(request ,id):
    patient = Test.objects.get(id=id)
    patient.delete()
    
    return redirect('testmaster')
@device_required
def scan(request,id):
    scans = Visit.objects.get(id=id)
    context = {
        'scans':scans,
    }
    return render(request,'scan.html',context)

@login_required
@device_required
def scansummary(request):
    return render(request,'scansummary.html')

@login_required
@device_required
def telepathreport(request):
    return render(request,'telepathreport.html')

@login_required
@device_required
def addrefdr(request):
    if 'DoctorCode' not in request.session:
        request.session['DoctorCode'] = generate_Doctoruhid()
    if request.method == 'POST':
       DoctorName=  request.POST.get('DoctorName')
       Qualification=  request.POST.get('Qualification')
       Specialisation=  request.POST.get('Specialisation')
       Address=  request.POST.get('Address')
       PINCode=  request.POST.get('PINCode')
       Mobile=  request.POST.get('Mobile')
       EmailID=  request.POST.get('EmailID')
       refdr = RefDr(DoctorCode=request.session['DoctorCode'] ,DoctorName= DoctorName ,Qualification =Qualification ,Specialisation =Specialisation,Address =Address ,PINCode= PINCode ,Mobile =Mobile ,EmailID=EmailID)
       refdr.save()
       
       request.session['DoctorCode'] = generate_Doctoruhid()
       return redirect('refdrmaster')
       
    return render(request,'Refdr.html',{'DoctorCode': request.session['DoctorCode']})

@login_required
@device_required
def refdrmaster(request):
    refdrmaster = RefDr.objects.all()
    
    
    if request.method == 'POST':
        DoctorCode = request.POST.get('DoctorCode')
        DoctorName = request.POST.get('DoctorName')
        Qualification = request.POST.get('Qualification')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        # Filter by visit id
        if DoctorCode:
            refdrmaster = refdrmaster.filter(DoctorCode__icontains=DoctorCode)
        
        # Filter by status
        if DoctorName:
            refdrmaster = refdrmaster.filter(DoctorName__icontains=DoctorName)
            
        if Qualification:
            refdrmaster = refdrmaster.filter(Qualification__icontains=Qualification)
        
        # Filter by date range
        if from_date and to_date:
            refdrmaster = refdrmaster.filter(date__range=[from_date, to_date])
        
        
        context = {'refdrmaster': refdrmaster, 'from_date': from_date, 'to_date': to_date}
        
    else:
        
      context = {
        'refdrmaster':refdrmaster,
      }
    return render(request,'RefDrmaster.html',context)

@login_required
@device_required
def edit_refdr(request, id):
    refdr = RefDr.objects.get(id=id)
    if request.method == 'POST':
        # Save the updated data to the database
        refdr.DoctorCode = request.POST.get('DoctorCode')
        refdr.DoctorName = request.POST.get('DoctorName')
        refdr.Qualification = request.POST.get('Qualification')
        refdr.Specialisation = request.POST.get('Specialisation')
        refdr.Address = request.POST.get('Address')
        refdr.PINCode = request.POST.get('PINCode')
        refdr.Mobile = request.POST.get('Mobile')
        refdr.EmailID = request.POST.get('EmailID')
        refdr.save()
        return redirect('refdrmaster')
    else:
        # Render the edit form with the current data filled in
        return render(request, 'edit_refdr.html', {'refdr': refdr})

@login_required
@device_required
def edittest(request, id):
    edittest = Test.objects.get(id=id)
    if request.method == 'POST':
           edittest.testid = request.POST.get('testid')
           edittest.name = request.POST.get('name')
           edittest.specimen_type = request.POST.get('specimen_type')
           edittest.department = request.POST.get('department')
           edittest.report_format = request.POST.get('report_format')
           edittest.reporting_rate = request.POST.get('reporting_rate')
           edittest.save()
           return redirect('testmaster')
    else:
        # Render the edit form with the current data filled in
     return render(request, 'edittest.html', {'edittest': edittest})
 
 





import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import barcode
from barcode.writer import ImageWriter
import os
from reportlab.lib.utils import ImageReader

@login_required
@device_required
def downloadbarcode(request, patient_id):
    patient = ekon.objects.get(id=patient_id)

    # Generate PDF with barcode and patient details
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 12)

    # Calculate the center positions
    page_width, page_height = A4
    center_x = page_width / 2
    center_y = page_height / 2

    # Draw patient details
    text_height = 20
    c.drawString(center_x, center_y + 50, f" {patient.patient_name}")
    c.drawString(center_x, center_y + 50 - text_height, f"Age: {patient.age}")
    c.drawString(center_x, center_y + 50 - 2 * text_height, f"Gender: {patient.gender}")

    # Add barcode image using the accession number
    barcode_data = patient.accession_number
    barcode_image = barcode.get('code128', barcode_data, writer=ImageWriter()).render()
    barcode_image_reader = ImageReader(barcode_image)

    # Draw barcode image on the PDF canvas
    barcode_width = 200
    barcode_height = 100
    barcode_x = center_x - (barcode_width / 2)
    barcode_y = center_y - (barcode_height / 2)
    c.drawImage(barcode_image_reader, barcode_x, barcode_y, width=barcode_width, height=barcode_height)

    c.showPage()
    c.save()

    # Rewind the buffer and create an HTTP response with the PDF data
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=barcode.pdf'
    return response



# APIs
class ekonViewSet(viewsets.ModelViewSet):
    queryset = ekon.objects.all()
    serializer_class = ekonSerializer
    
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    
class RefDrViewSet(viewsets.ModelViewSet):
    queryset = RefDr.objects.all()
    serializer_class = RefDrSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    
class patientcategoryViewSet(viewsets.ModelViewSet):
    queryset = patientcategory.objects.all()
    serializer_class = patientcategorySerializer
    
class ScansummaryViewSet(viewsets.ModelViewSet):
    queryset = Scansummary.objects.all()
    serializer_class = ScansummarySerializer
    