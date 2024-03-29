import os
from django.shortcuts import redirect
from .models import Test,ekon,RefDr,Visit
import re
import uuid


def generate_accession_number():
    last_accession = ekon.objects.order_by('-id').first()
    
    if last_accession:
        last_accession_id = int(last_accession.accession_number.split('-')[-1])
        new_accession_id = str(last_accession_id + 1)
    else:
        new_accession_id = '100001'
    
    return new_accession_id.zfill(6)




 



# def generate_uhid():
    
#    last_patient_id = ekon.objects.order_by('-id').first()
#    if last_patient_id:
#         last_Pid = int(last_patient_id.uhid.split('P')[-1])
#         new_Pid = f'P{last_Pid+1:05}'
#    else:
#         new_Pid = 'P00001'
#    return new_Pid


def generate_uhid():
    last_uhid = ekon.objects.order_by('-id').first()
    if last_uhid:
        last_uhid = int(last_uhid.uhid.split('P')[-1])
        new_uhid = f'P{last_uhid+1:05}'
    else:
        new_uhid = 'P00001'
    return new_uhid





def generate_testuhid():
    last_test_id = Test.objects.order_by('-id').first()
    if last_test_id:
        last_id = int(last_test_id.testid.split('T')[-1])
        new_id = f'T{last_id+1:05}'
    else:
        new_id = 'T00001'
    return new_id




def generate_visit_id():
   last_visit_id = Visit.objects.order_by('-id').first()
   if last_visit_id:
        last_Vid = int(last_visit_id.visit_id.split('V')[-1])
        new_Vid = f'V{last_Vid+1:05}'
   else:
        new_Vid = 'V00001'
   return new_Vid


def generate_Doctoruhid():
    latest_doctor_code = RefDr.objects.filter(
        DoctorCode__regex=r'^D\d{5}$'
    ).order_by('-DoctorCode').first()

    if latest_doctor_code:
        latest_did = int(latest_doctor_code.DoctorCode.split('D')[-1])
        new_did = f'D{latest_did+1:05d}'
    else:
        new_did = 'D00001'

    return new_did



