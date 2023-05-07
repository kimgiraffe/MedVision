from rest_framework import serializers
from .models import User, Prescription, Schedule, DrugDetail, DrugHour

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['userId', 'userRealName', 'userEmail']

class PrescriptionSerializer(serializers.Serializer):
    # prescId = serializers.DecimalField
    # prescDate = serializers.DateField
    # dispensary = serializers.CharField
    class Meta:
        model = Prescription
        fields = '__all__'

class ScheduleSerializer(serializers.Serializer):
    prescDate = serializers.ReadOnlyField(source='prescId.prescDate')
    dispensary = serializers.ReadOnlyField(source='prescId.dispensary')
    class Meta:
        model = Schedule
        fields = ['startDate', 'endDate', 'prescDate', 'dispensary']

class DrugDetailSerializer(serializers.Serializer):
    class Meta:
        model = DrugDetail
        fields = ['drugName', 'drugEffect', 'quantity', 'dosagePerOnce', 'dailyDose', 'totalDosingDays', 'startDate']

class DrugHourSerializer(serializers.Serializer):
    drugName = serializers.ReadOnlyField(source='drugId.drugName')
    class Meta:
        model = DrugHour
        fields = ['drugName', 'hour']
