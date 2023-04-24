from django.shortcuts import redirect

class DeviceRegistrationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated or not request.user.is_device_registered:
            if not request.path.startswith('/register_device'):
                return redirect('register_device')

        response = self.get_response(request)
        return response
