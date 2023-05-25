from rest_framework import serializers
from django.contrib.auth import models, authenticate, login
from .models import User, Prescription, DrugInfo, PrescDetail, Schedule, DrugHour

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'userRealName', 'userEmail', 'userPassword']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)

        if username and password:
            try:
                user = User.objects.get(userId=username)
                if password == user.userPassword:
                    print('로그인 성공')
                    return data
                else:
                    raise serializers.ValidationError("아이디 또는 비밀번호가 틀립니다")
                    
            except User.DoesNotExist:
                    raise serializers.ValidationError("아이디 또는 비밀번호가 틀립니다")
        else:
            raise serializers.ValidationError("아이디와 비밀번호를 모두 입력하세요")
 

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('userId', 'userPassword', 'password2', 'userEmail','userRealName')

    def validate(self, attrs):
        if attrs['userPassword'] != attrs['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다")
        
        if User.objects.filter(userId=attrs['userId']).exists():
            raise serializers.ValidationError("가입된 Id 입니다.")

        
        if User.objects.filter(userEmail=attrs['userEmail']).exists():
            raise serializers.ValidationError("가입된 email 입니다.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        username = validated_data.pop('userId')
        password = validated_data.pop('userPassword')
        print(f"{username}님 회원가입을 축하합니다!")
        return user


class UserUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20)
    password2 = serializers.CharField(max_length=20)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password and password2:
            if password != password2:
                raise serializers.ValidationError( "비밀번호가 일치하지 않습니다")
            return attrs
        else :
            raise serializers.ValidationError("비밀번호를 입력해주세요")
       


class DrugInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugInfo
        fields = '__all__'

class PrescDetailSerializer(serializers.ModelSerializer):
    drugName = serializers.ReadOnlyField(source='drugInfo.drugName')

    class Meta:
        model = PrescDetail
        fields =('drugName',
                'dosagePerOnce',
                'dailyDose',
                'totalDosingDays')

class PrescriptionSerializer(serializers.ModelSerializer):
    def get_details(self, obj):
        details = PrescDetail.objects.filter(prescription=obj)
        serializer = PrescDetailSerializer(details, many=True)

        return serializer.data
    
    details = serializers.SerializerMethodField('get_details')

    class Meta:
        model = Prescription
        fields = ('prescId', 'details', 'prescDate', 'dispensary')

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class DrugHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugHour
        fields = '__all__'



