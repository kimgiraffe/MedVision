import django.db.utils
from django.contrib.auth import login, logout, authenticate, models
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse 
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Prescription, PrescDetail, DrugInfo, Schedule
from .serializers import UserSerializer, PrescriptionSerializer, PrescDetailSerializer, DrugInfoSerializer, ScheduleSerializer,\
LoginSerializer, RegisterSerializer, UserUpdateSerializer, ScheduleUpdateSerializer
from rest_framework import generics, status
from datetime import datetime, timedelta

# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
# class LoginView(APIView):
#     """
#       API View for login through a POST request.
#       """
#     def post(self, request):
#         username = request.data.get('id')
#         password = request.data.get('password')
#         loginUser = UserAuth.authenticate(userId=username, userPassword=password)

#         if loginUser is not None:
#             print('로그인 성공')
#             user = authenticate(username=username, password=password)
#             login(request, user=user)
#             serializer = UserSerializer(loginUser)
#             print(request.user)
#             print(request.headers)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "아이디 또는 비밀번호가 틀립니다."}, status=status.HTTP_401_UNAUTHORIZED)

# class UserAuth:
#     def authenticate(userId=None, userPassword=None):
#         try:
#             user = User.objects.get(userId=userId)
#             if userPassword == user.userPassword:
#                 return user
#         except User.DoesNotExist:
#             return None

# class RegisterView(APIView):
#     """
#       API View to create or get a list of all the registered
#       users. GET request returns the registered users whereas
#       a POST request allows to create a new user.
#       """
#     def get(self, format=None):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         username = request.data.get('id')
#         password = request.data.get('password')
#         email = request.data.get('email')
#         try:
#             createUser = User(userId=username, userPassword=password, userEmail=email)
#             createUser.save()
#             AuthUser(username=username, password=password).save()
#         except django.db.utils.IntegrityError as e:
#             if 'userId' in e.args[0]:
#                 print("아이디가 이미 사용중입니다!")
#             if 'userEmail' in e.args[0]:
#                 print("이메일이 이미 사용중입니다!")
#             return Response(status=status.HTTP_401_UNAUTHORIZED)

#         loginUser = UserAuth.authenticate(userId=username, userPassword=password)
#         if loginUser is not None:
#             user = authenticate(username=username, password=password)
#             login(request, user=user)
#             print(f"{user}님! 회원가입을 축하합니다")
#             login(request, user=user, backend='users.views.UserAuth')
#             serializer = UserSerializer(loginUser)
#             return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save()
        print(serializer)
        username = serializer.data['userId']
        password = serializer.data['userPassword']
        models.User(username=username, password=make_password(password)).save()
        loginUser = authenticate(username=username, password=password)
        login(self.request, user=loginUser)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        loginUser = authenticate(request, username=user['username'], password=user['password'])
        print(loginUser)
        login(request, loginUser)
        print(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    def get(self, request):
        print(request.user)
        logout(request)
        print(request.user)
    
        return Response(status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            password = request.data['password']
            userId = request.user

            user = User.objects.get(userId=userId)

            if password == user.userPassword:
                return Response({"message": "새로운 비밀번호를 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
            model_user = models.User.objects.get(username=userId)
             # 비밀번호 변경
            logout(request)
            user.userPassword = password
            user.save()
            model_user.password = make_password(password)
            model_user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        userId = request.user

        if userId.is_authenticated:
            user = User.objects.get(userId=userId)
            model_user = models.User.objects.get(username=userId)

            user.delete()
            model_user.delete()

            return Response({"message": "탈퇴되었습니다."},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
 

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PrescriptionListView(generics.RetrieveAPIView):

    def get(self, request):
        # 로그인된 사용자 정보 가져오기
        user = User.objects.get(userId=request.user)
        print(request.user)
        print(request.user.is_authenticated)
        # Serializer에서 해당 사용자의 정보 검색
        queryset = Prescription.objects.filter(user=user)

        # Serializer를 사용하여 응답 데이터 직렬화
        serializer = PrescriptionSerializer(queryset, many=True)
        return Response(serializer.data)

class DrugInfoView(APIView):
    def get(self, request):
        # 알약 일렬번호 가져오기
        drugNo = request.data['drugNo']

        #Serializer에서 해당 알약의 정보 검색
        queryset = DrugInfo.objects.filter(drugNo=drugNo)

        #Serializer를 사용하여 응답 데이터 직렬화
        serializer = DrugInfoSerializer(queryset)
        return Response(serializer.data)
    
class PrescDetailListView(generics.ListAPIView):
    def get(self, request):
        # 처방번호 가져오기
        prescId = request.data['prescId']
        prescription = Prescription.objects.get(prescId=prescId)

        # Serializer에서 해당 처방내역 정보 검색
        queryset = PrescDetail.objects.filter(prescription=prescription)

        # Serializer를 사용하여 응답 데이터 직렬화
        serializer = PrescDetailSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ScheduleListView(generics.ListAPIView):
    # 일정 목록을 보여줄 때
    def get(self, request):
        # 로그인된 사용자 정보 가져오기
        user = User.objects.get(userId=request.user)

        # Serializer에서 해당 사용자의 처방내역 검색
        queryset = Schedule.objects.filter(user=user)

        # Serializer를 사용하여 응답 데이터 직렬화
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

    # 새로운 일정을 등록할 때
    def post(self, request):
        # 처방내역 선택
        prescId = request.data['prescId']
        prescription = Prescription.objects.get(prescId=prescId)
    
        startDateStr = request.data['startDate']

        # 일정 종료일자 검색 (처방내역에서 계산)
        items = prescription.prescdetails
        maxDosingDays = 0
        for i in items:
            if i.totalDosingDays > max:
                maxDosingDays = int(i)

        startDate = datetime.strptime(startDate,startDate).date()
        endDate = startDate + timedelta(days=maxDosingDays)

        Schedule(prescription=prescription, startDate=startDate, endDate=endDate).save()
        

class ScheduleDetailView(APIView):
    def get_schedule(self, request):
         # 처방번호 가져오기
        prescId = request.data['prescId']
        prescription = Prescription.objects.get(prescId=prescId)

        # Serializer에서 해당 검색
        queryset = PrescDetail.objects.filter(prescription=prescription)


class ScheduleDeleteView(APIView):
    def delete(self, request, presc_id):
        try:
            schedule = Schedule.objects.get(prescription__prescId=presc_id)
        except Schedule.DoesNotExist:
            return Response({'message': '복용 일정을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        if schedule.prescription.user != request.user:
            schedule.delete()
        return Response({'message': '복용 일정이 삭제되었습니다'}, status=status.HTTP_204_NO_CONTENT)


class ScheduleUpadateView(APIView):
    serializer_class = ScheduleUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, presc_id):
        schedule = Schedule.objects.get(prescription__prescId=presc_id)
        serializer = self.serializer_class(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
"""     
  login via web 
  """
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
