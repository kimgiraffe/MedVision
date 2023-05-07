import os, base64
import requests
from .암호화 import aesEncrypt, rsaEncrypt, getPublicKey
from .간편인증 import simpleAuth
from .낱알정보 import getPillInfo
from .api_param import API_Param
from users.models import Prescription, DrugInfo, PrescDetail, PillData

def getPrescription(apiHost, apiKey, apiParam):
    # RSA Public Key 조회
    rsaPublicKey = getPublicKey()
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
    reqData = simpleAuth(apiHost, apiKey, apiParam)
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

    if Prescription.objects.count() != 0:
        latestPrescId = Prescription.objects.latest('prescId').prescId
    print(latestPrescId)

    # prescIdList = []
    # 지난 1년 처방이력 출력
    for i in resultList:
        print(f"조제일자: {i['DateOfPreparation']}")
        # 처방건 리스트 추가
        # prescIdList.append(i['No'])

        # Prescription 모델 DB에 저장
        id = i['No']
        if i['No'] != str(latestPrescId) or latestPrescId is None:
            Prescription(prescId=id, prescDate=i['DateOfPreparation'], dispensary=i['Dispensary']).save()
            # 처방내역 정보 DB에 저장
            for j in i['DrugList']:
                ediCode = j['Code']
                print(j)
                print(j['Code'])
                # getPillInfo(id, ediCode)

                # 처방내역의 약물 정보 DB에 저장
                DrugInfo(
                    drugNo=ediCode,
                    drugName=j['Name'],
                    drugEffect=j['Effect'],
                    component=j['Component'],
                    quantity=j['Quantity'],
                ).save()

                PrescDetail(
                    prescId=id,
                    drugNo=ediCode,
                    dosagePerOnce=j['DosagePerOnce'],
                    dailyDose=j['DailyDose'],
                    totalDosingDays=j['TotalDosingDays']
                ).save()
        else: break

    # return prescIdList

