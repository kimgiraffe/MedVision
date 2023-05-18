from rest_framework import serializers
from .models import User, Prescription, DrugInfo, PrescDetail, Schedule, DrugHour

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'userRealName', 'userEmail']

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('userId', 'userPassword', 'password2', 'userRealName', 'userEmail', 'userRegisterDatetime')


    def validate(self, attrs):
        if attrs['userPassword'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "비밀번호가 일치하지 않습니다"
            })
        
        if User.objects.filter(userId=attrs['userId']).exists():
            raise serializers.ValidationError("가입된 Id 입니다.")

        
        if User.objects.filter(userEmail=attrs['userEmail']).exists():
            raise serializers.ValidationError("가입된 email 입니다.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        return user


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
