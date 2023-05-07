import requests
from users.models import PillData
def getPillInfo(presc_id, pill_edi_code):
    url = 'http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01'
    params ={'serviceKey' : 'XhzWrdnyXRykvCEJSiPqWWjHuP7u5stjflVUZ81wQeY2mTRWNLloRMZsBTeiViMmiCjFw1xAxUfKf5FyXJaxuQ==', 'item_name' : '', 'entp_name' : '', 'item_seq' : '', 'img_regist_ts' : '', 'pageNo' : '1', 'numOfRows' : '3', 'edi_code' : pill_edi_code, 'type' : 'json' }

    response = requests.get(url, params=params).json()
    if response['body']['totalCount'] != 0:
        responseItem = response['body']['items'][0]

        color = ''
        if(responseItem["COLOR_CLASS1"] is not None):
            color = responseItem["COLOR_CLASS1"]
        if(responseItem["COLOR_CLASS2"] is not None):
            if color == '':
                color = responseItem["COLOR_CLASS1"]
            else:
                color = color + ' ' + responseItem["COLOR_CLASS2"]

        shape = responseItem["DRUG_SHAPE"]

        text = ''
        if (responseItem["PRINT_FRONT"] is not None):
            text = responseItem["PRINT_FRONT"]
        if (responseItem["PRINT_BACK"] is not None):
            if text == '':
                text = responseItem["PRINT_BACK"]
            else:
                text = text + ' ' + responseItem["PRINT_BACK"]

        print(f'{color} {shape} {text}')
        PillData(prescId=presc_id, drugNo=pill_edi_code, pillShape=shape, pillColor=color, pillText=text).save()
