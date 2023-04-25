from django.shortcuts import redirect
from django.urls import reverse
from .models import Device

class DeviceRegistrationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            # Check if user has a registered device
            if Device.objects.filter(user=user, is_registered=True).exists():
                pass
            else:
                # Redirect to device registration page if device is not registered
                return redirect('register_device')
        else:
            # Redirect to login page if user is not authenticated
            return redirect(reverse('login') + '?next=' + request.path)

        response = self.get_response(request)
        return response
