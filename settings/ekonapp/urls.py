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
    path('refdr/',refdr,name='refdr'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)