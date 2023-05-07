from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.api_param import API_Param
from .처방내역 import getPrescription
from users.models import User
import sys

# Create your views here.
def main(request):
    return HttpResponse("MedVision")


# @api_view(['GET'])
# def get_drug_info(request):

@api_view(['GET', 'POST'])
def createLoginView(request):
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
        getPrescription(apiParam._apiHost, apiParam._apiKey, apiParam)

        # DB에 회원 실명 등록
        if(User.objects.count() == 1):
            user = User.objects.first()
            if user.userRealName == '':
                user.userRealName = username
                user.save()

        return JsonResponse(data=request.POST)
