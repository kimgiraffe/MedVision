import os, base64
import requests
from .암호화 import aesEncrypt, rsaEncrypt, getPublicKey
from .api_param import API_Param

# API 호출
def simpleAuth(apiHost, apiParam):
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
    url = apiHost + "api/v1.0/hirasimpleauth/simpleauthrequest"

    # API 요청 파라미터 설정
    options = {
        "headers": {
            "Content-Type": "application/json",
            "API-KEY": apiKey,
            "ENC-KEY": aesCipherKey
        },

        "json": {
            "PrivateAuthType": "4",
            "UserName": aesEncrypt(aesKey, aesIv, apiParam.myUsername),
            "BirthDate": aesEncrypt(aesKey, aesIv, apiParam.myBirthdate),
            "UserCellphoneNumber": aesEncrypt(aesKey, aesIv, apiParam.myCellphoneNumber),
            "IdentityNumber": aesEncrypt(aesKey, aesIv, apiParam.myIdentityNumber),
        },
    }

    res = requests.post(url, headers=options['headers'], json=options['json'])
    print(f"res: {res.json()}")
    return res.json()["ResultData"]
