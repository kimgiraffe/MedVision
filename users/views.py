from django.shortcuts import render, redirect
from .models import User, Prescription, DrugInfo
from .serializers import UserSerializer, PrescriptionSerializer, DrugInfoSerializer
from django.http import HttpResponse
from rest_framework import generics

# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def index(request):
    if request.method == 'GET':
        print('Start MedVision')
        return render(request, 'login.html')

    elif request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')

        res_data = {}

        if not (id and password):
            res_data['error'] = '아이디 또는 비밀번호를 입력하세요'
        else:
            loginUser = User.objects.get(userId=id)
            if password == loginUser.userPassword:
                request.session['userId'] = id
                return redirect('/api/authenticate')
            else: res_data['error'] = '비밀번호를 다시 입력하세요'

        return render(request, 'login.html', res_data)

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

# def PrescList(request):
#     user = User.objects.get(userId=request.session['userId'])
#     if request.method == 'GET':
#

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PrescriptionView(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class DrugInfoView(generics.ListCreateAPIView):
    queryset = DrugInfo.objects.all()
    serializer_class = DrugInfoSerializer