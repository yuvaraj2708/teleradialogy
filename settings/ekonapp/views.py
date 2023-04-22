from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
import uuid
from django.http import HttpResponse
from .utils import generate_uhid,generate_testuhid,generate_Doctoruhid
from django.db.models import Q
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
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
        return redirect('registrationsummary')
    return render(request, 'patient-registration.html', {'uhid': request.session['uhid']})





@login_required
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
def register_device(request):
    user = request.user
    
    if user.is_device_registered:
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
                # Device has already been registered, show error message
                return render(request, 'error.html', {'message': 'Device has already been registered.'})
        except Device.DoesNotExist:
            pass
        
        # Create a new device object
        device = Device(device_id=device_id, client_name=client_name, address=address, pin_code=pin_code, mobile_number=mobile_number, email=email)
        device.save()
        
        # Update user's device registration status
        user.is_device_registered = True
        user.save()
        
        # Set device authentication status to True
        device.is_authenticated = True
        device.save()
        
        # Redirect to registration summary
        return redirect('registrationsummary')
    else:
        # Check if device is already authenticated
        device_id = request.GET.get('device_id')
        if device_id:
            try:
                device = Device.objects.get(device_id=device_id)
                if device.is_authenticated:
                    # Device is already authenticated, redirect to desired page
                    return redirect('desiredpage')
            except Device.DoesNotExist:
                pass
        
        # Render registration form
        return render(request, 'registerdevice.html')


@login_required
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

@login_required
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


#    PatientCategory = models.CharField(max_length=255)
#     Refdr = models.ForeignKey(RefDr,on_delete=models.CASCADE)
#     Selecttest = models.ForeignKey(Test,on_delete=models.CASCADE)
    
    
@login_required
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




def delete(request, id):
    patient = ekon.objects.get(id=id)
    
    patient.delete()
    return redirect('registrationsummary')

def delete(request, id):
    patient = Visit.objects.get(id=id)
    
    patient.delete()
    return redirect('visitsummary')

def delete(request, id):
    patient = RefDr.objects.get(id=id)
    
    patient.delete()
    return redirect('refdrmaster')



def scan(request):
    return render(request,'scan.html')


def scansummary(request):
    return render(request,'scansummary.html')


def telepathreport(request):
    return render(request,'telepathreport.html')

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


class DeviceRegistrationView(TemplateView):
    template_name = 'device_registration.html'

    def get(self, request, *args, **kwargs):
        device_id = kwargs.get('device_id')
        try:
            device = Device.objects.get(device_id=device_id)
            if device.is_registered:
                return HttpResponseRedirect(reverse('main'))
            else:
                return super().get(request, *args, **kwargs)

        except Device.DoesNotExist:
            return HttpResponseRedirect(reverse('device_login'))
    
    def post(self, request, *args, **kwargs):
        device_id = kwargs.get('device_id')
        try:
            device = Device.objects.get(device_id=device_id)
            device.is_registered = True
            device.save()
            return HttpResponseRedirect(reverse('main'))

        except Device.DoesNotExist:
            return HttpResponseRedirect(reverse('device_login'))
