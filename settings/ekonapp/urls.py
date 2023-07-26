from django.urls import path 
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView




urlpatterns = [
    
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('Dashboard/',Dashboard,name="Dashboard"),
    path('Settings/',Settings,name="Settings"),
    path('',registerlogin,name='registerlogin'),
    path('patientregistration/',patientregistration,name='patient-registration'),
    path('editpatient/',editpatient,name='editpatient'),
    path('addvisit/<int:id>/', addvisit, name='addvisit'),
    path("delete/<int:id>/" ,delete,name= "delete"),
    path('deleteregistersummary/<int:id>/',deleteregistersummary,name="deleteregistersummary"),
    path('deletetest/<int:id>/',deletetest,name="deletetest"),
    path('deletevisit/<int:id>/',deletevisit,name="deletevisit"),
    path('registersummary/',registrationsummary,name='registrationsummary'),
    path('visitsummary/',visitsummary,name='visitsummary'),
    path('register_device/',register_device,name="register_device"),
    path('testmaster/',testmaster,name='testmaster'),
    path('addtest/',addtest,name='addtest'),
    path('telepathreport/',telepathreport,name="telepathreport"),
    path('scan/<int:id>/',scan,name='scan'),
    path('scansummary/',scansummary,name='scansummary'),
    path('pathologist_mst/',addrefdr,name='refdr'),
    path('refdrmaster/',refdrmaster,name='refdrmaster'),
    path('edit_refdr/<int:id>/',edit_refdr,name="edit_refdr"),
    path('edittest/<int:id>/',edittest,name='edittest'),
    path('downloadbarcode/<int:patient_id>/', downloadbarcode, name='downloadbarcode'),
  

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)