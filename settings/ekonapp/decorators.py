from django.shortcuts import redirect
from .models import Device 

def device_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # If the user is not authenticated, redirect to login page
            return redirect('registerlogin')
        elif not Device.objects.filter(user=request.user, is_registered=True).exists():
            # If the user has not registered a device, redirect to register device page
            return redirect('register_device')
        else:
            # If the user has registered a device, call the view function
            return view_func(request, *args, **kwargs)

    return wrapper
