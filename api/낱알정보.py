import requests
from users.models import PillData
from time import sleep

def getPillData(drugNo):
    url = 'http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01'
    params ={'serviceKey' : 'XhzWrdnyXRykvCEJSiPqWWjHuP7u5stjflVUZ81wQeY2mTRWNLloRMZsBTeiViMmiCjFw1xAxUfKf5FyXJaxuQ==', 'item_name' : '', 'entp_name' : '', 'item_seq' : '', 'img_regist_ts' : '', 'pageNo' : '1', 'numOfRows' : '1', 'edi_code' : drugNo, 'type' : 'json' }

    try:
        response = requests.get(url, params=params, verify=False).json()
    except:
        sleep(1)
        response = requests.get(url, params=params, verify=False).json()

    if response['body']['totalCount'] != 0:
        pillData = response['body']['items'][0]

        color = ''
        if(pillData["COLOR_CLASS1"] is not None):
            color = pillData["COLOR_CLASS1"]
        if(pillData["COLOR_CLASS2"] is not None):
            if color == '':
                color = pillData["COLOR_CLASS1"]
            else:
                color = color + ' ' + pillData["COLOR_CLASS2"]

        shape = pillData["DRUG_SHAPE"]

        text = ''
        if (pillData["PRINT_FRONT"] is not None):
            text = pillData["PRINT_FRONT"]
        if (pillData["PRINT_BACK"] is not None):
            if text == '':
                text = pillData["PRINT_BACK"]
            else:
                text = text + ' ' + pillData["PRINT_BACK"]

        print(f'{color} {shape} {text}')
        PillData(drugNo=drugNo, pillShape=shape, pillColor=color, pillText=text).save()