import os
from django.shortcuts import redirect
from .models import Test,ekon,RefDr
import re
import uuid


def generate_uhid():
    # Set the starting ID as 1
    start_id = 1
    
    # Check if the file with the last used ID exists
    if os.path.exists('last_uhid.txt'):
        # If it does, read the last used ID from the file
        with open('last_uhid.txt', 'r') as f:
            last_uhid = int(f.read().strip())
    else:
        # If the file doesn't exist, start with the specified ID
        last_uhid = start_id - 1
    
    # Increment the last used ID and generate the new ID
    new_uhid = f'P{last_uhid+1:05}'
    
    # Write the new last used ID to the file
    with open('last_uhid.txt', 'w') as f:
        f.write(str(last_uhid + 1))
    
    return new_uhid


# def generate_uhid():
#     last_uhid = ekon.objects.order_by('-id').first()
#     if last_uhid:
#         last_uhid = int(last_uhid.uhid.split('P')[-1])
#         new_uhid = f'P{last_uhid+1:05}'
#     else:
#         new_uhid = 'P00001'
#     return new_uhid





def generate_testuhid():
    last_test_id = Test.objects.order_by('-id').first()
    if last_test_id:
        last_id = int(last_test_id.testid.split('T')[-1])
        new_id = f'T{last_id+1:05}'
    else:
        new_id = 'T00001'
    return new_id




def generate_visit_id():
    # Generate a UUID and extract the numerical portion
    uuid_num = int(re.sub('[^0-9]', '', uuid.uuid4().hex))
    # Pad the numerical portion with leading zeros to 5 digits
    visit_num = str(uuid_num).zfill(5)
    # Concatenate the numerical portion with the letter "V"
    visit_id = f'V{visit_num}'
    return visit_id


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


