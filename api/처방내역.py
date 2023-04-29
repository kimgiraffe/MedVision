import os, base64
import requests
from .암호화 import aesEncrypt, rsaEncrypt, getPublicKey
from .간편인증 import simpleAuth
from .api_param import API_Param
from users.models import Presc

def getPrescrption(apiHost, apiKey, apiParam):
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
    print("success")
    res = requests.post(url, headers=options['headers'], json=options['json'])
    # print(f"res: {res.json()}")
    resultList = res.json()["ResultList"]
    prescList = []

    # 처방이력 출력
    for i in resultList:
        print("처방일자: " + i["DateOfPreparation"])
        prescList.append(i["No"])
        for j in i["DrugList"]:
            print(j)

    # 처방건 일련번호 DB에 저장
    # latest = Presc.objects.get(id=1).prescNo
    # for k in prescList:
    #     if latest is not None and k == latest: break
    #     Presc.objects.create(prescNo=k)
    #



