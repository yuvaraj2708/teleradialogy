from rest_framework import serializers
from .models import *

class ekonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ekon
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        
class RefDrSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefDr
        fields = '__all__'
        
class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
        
class patientcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = patientcategory
        fields = '__all__'
        
class ScansummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Scansummary
        fields = '__all__'