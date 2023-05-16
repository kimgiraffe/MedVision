from rest_framework import serializers
from .models import User, Prescription, DrugInfo, PrescDetail, Schedule, DrugHour

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'userRealName', 'userEmail']

class PrescriptionSerializer(serializers.ModelSerializer):
    # prescId = serializers.DecimalField
    # prescDate = serializers.DateField
    # dispensary = serializers.CharField
    class Meta:
        model = Prescription
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    prescDate = serializers.ReadOnlyField(source='prescription.prescDate')
    dispensary = serializers.ReadOnlyField(source='prescription.dispensary')
    class Meta:
        model = Schedule
        fields = ['startDate', 'endDate', 'prescDate', 'dispensary']

class DrugInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugInfo
        fields = '__all__'

class PrescDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescDetail
        fields = ['dosagePerOnce', 'dailyDose', 'totalDosingDays', 'startDate']

class DrugHourSerializer(serializers.ModelSerializer):
    drugName = serializers.ReadOnlyField(source='drugId.drugName')
    class Meta:
        model = DrugHour
        fields = ['drugNo', 'hour']
