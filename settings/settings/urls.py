"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from ekonapp.views import *

router = routers.DefaultRouter()
router.register(r'ekons', ekonViewSet)
router.register(r'Device', DeviceViewSet)
router.register(r'Test', TestViewSet)
router.register(r'RefDr', RefDrViewSet)
router.register(r'Visit', VisitViewSet)
router.register(r'patientcategory', patientcategoryViewSet)
router.register(r'Scansummary', ScansummaryViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ekonapp.urls')),
    path('api/', include(router.urls)),
   
]
