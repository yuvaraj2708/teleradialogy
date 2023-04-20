import os
from django.shortcuts import redirect

def generate_uhid():
    # Check if the file with the last used ID exists
    if os.path.exists('last_uhid.txt'):
        # If it does, read the last used ID from the file
        with open('last_uhid.txt', 'r') as f:
            last_uhid = int(f.read().strip())
    else:
        # If the file doesn't exist, start with ID 1
        last_uhid = 0
    
    # Increment the last used ID and generate the new ID
    new_uhid = str(last_uhid + 1).zfill(6)
    
    # Write the new last used ID to the file
    with open('last_uhid.txt', 'w') as f:
        f.write(new_uhid)
    
    return new_uhid



def require_purchase(func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.has_purchased_access:
            return func(request, *args, **kwargs)
        else:
            return redirect('purchase')
    return wrapper