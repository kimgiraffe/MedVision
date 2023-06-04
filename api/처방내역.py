import os, base64
import requests
from .암호화 import aesEncrypt, rsaEncrypt, getPublicKey
from .간편인증 import simpleAuth
from .낱알정보 import getPillData
from django.db.models import Q
from django.http import JsonResponse
from users.models import Prescription, DrugInfo, PrescDetail, PillData

def getPrescription(user, apiParam):
    apiHost = apiParam._apiHost
    apiKey = apiParam._apiKey

    # RSA Public Key 조회
    rsaPublicKey = getPublicKey(apiKey)
    print(f"rsaPublicKey: {rsaPublicKey}")

    # AES Secret Key 및 IV 생성
    aesKey = os.urandom(16)
    aesIv = ('\x00' * 16).encode('utf-8')

    # AES Key를 RSA Public Key로 암호화
    aesCipherKey = base64.b64encode(rsaEncrypt(rsaPublicKey, aesKey))
    print(f"aesCipherKey: {aesCipherKey}")

    # API URL 설정
    url = apiHost + "api/v1.0/hirasimpleauth/hiraa050300000100"

    # 간편인증 요청 후 받은 값 정리
    reqData = simpleAuth(apiHost, apiParam)
    print(f'res: {reqData}')

    # API 요청 파라미터 설정
    options = {
        "headers": {
            "Content-Type": "application/json",
            "API-KEY": apiKey,
            "ENC-KEY": aesCipherKey
        },

        "json": {
            "IdentityNumber": aesEncrypt(aesKey, aesIv, apiParam.myIdentityNumber),
            "CxId": reqData["CxId"],
            "PrivateAuthType": reqData["PrivateAuthType"],
            "ReqTxId": reqData["ReqTxId"],
            "Token": reqData["Token"],
            "TxId": reqData["TxId"],
            "UserName": aesEncrypt(aesKey, aesIv, reqData["UserName"]),
            "BirthDate": aesEncrypt(aesKey, aesIv, reqData["BirthDate"]),
            "UserCellphoneNumber": aesEncrypt(aesKey, aesIv, reqData["UserCellphoneNumber"]),
        },

    }

    # API 호출
    res = requests.post(url, headers=options['headers'], json=options['json'])
    resultList = res.json()["ResultList"]
    latestPrescId = None

    try:
        latestPrescId = Prescription.objects.filter(Q(user=user)).latest('prescId').prescId

    except Prescription.DoesNotExist:
        pass

    print(latestPrescId)

    # 지난 1년 처방이력 출력
    for i in resultList:
        print(f"조제일자: {i['DateOfPreparation']}")

        # Prescription 모델 DB에 저장
        prescId = i['No']
        if i['No'] != str(latestPrescId) or latestPrescId is None:
            prescItem = Prescription(user=user, prescId=prescId, prescDate=i['DateOfPreparation'], dispensary=i['Dispensary'])
            prescItem.save()

            # 처방내역 정보 DB에 저장
            for j in i['DrugList']:
                ediCode = j['Code']
                print(j)
                print(j['Code'])

                # 처방내역의 약물 정보 DB에 저장
                drugItem = DrugInfo(
                    drugNo=ediCode,
                    drugName=j['Name'],
                    drugEffect=j['Effect'],
                    component=j['Component'],
                    quantity=j['Quantity'],
                )
                drugItem.save()

                PrescDetail(
                    prescription=prescItem,
                    drugInfo=drugItem,
                    dosagePerOnce=j['DosagePerOnce'],
                    dailyDose=j['DailyDose'],
                    totalDosingDays=j['TotalDosingDays']
                    ).save()

                # 알약 특징 검색하고 DB에 저장
                if PillData.objects.filter(drugNo=ediCode).exists() == False:
                    getPillData(ediCode)
                else: pass

        else: break

