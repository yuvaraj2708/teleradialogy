from django.urls import path 
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('patientregistration/',patientregistration,name='patient-registration'),
    path('addvisit/<int:id>/', addvisit, name='addvisit'),
    path("delete/<int:id>/" ,delete,name= "delete"),
    path('registersummary/',registrationsummary,name='registrationsummary'),
    path('visitsummary/',visitsummary,name='visitsummary'),
    path('',register_device,name="register_device"),
    path('testmaster/',testmaster,name='testmaster'),
    path('addtest/',addtest,name='addtest'),
    path('telepathreport/',telepathreport,name="telepathreport"),
    path('scan/',scan,name='scan'),
    path('scansummary/',scansummary,name='scansummary'),
    path('pathologist_mst/',addrefdr,name='refdr'),
    path('refdrmaster/',refdrmaster,name='refdrmaster'),
    path('edit_refdr/<int:id>/',edit_refdr,name="edit_refdr"),
    path('edittest/<int:id>/',edittest,name='edittest'),
    path('devices/<str:device_id>/register/', DeviceRegistrationView.as_view(), name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)