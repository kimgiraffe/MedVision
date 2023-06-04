from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.api_param import API_Param
from .처방내역 import getPrescription
from .낱알정보 import getPillData
from users.models import User, PrescDetail
from time import sleep
import sys

# Create your views here.
def main(request):
    return HttpResponse("MedVision")

@api_view(['GET', 'POST'])
def authenticate(request):
    user = User.objects.get(userId=request.session['userId'])
    print(request.session['userId'])
    if request.method == 'GET':
        return render(request, "api/hira_authenticate.html")

    elif request.method == 'POST':
        print("ok")
        print(request.POST)

        username = request.POST['username']
        birthdate = request.POST['birthdate']
        cellphoneNumber = request.POST['cellphone'].replace('-', '')
        identityNumber = request.POST['identity']

        apiParam = API_Param(username, birthdate, cellphoneNumber, identityNumber)

        # 새로 처방이력 불러오고 등록된 약물 가져오기
        drugItemList = getPrescription(user, apiParam)

        # DB에 회원 실명 등록
        if user.userRealName == "":
            user.userRealName = username
            user.save()

        # return HttpResponse("받아오기 성공")
        return JsonResponse(data=request.POST)
