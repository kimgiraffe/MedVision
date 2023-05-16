from django.test import TestCase
import requests
# from users.models import PillData

# Create your tests here.

url = 'http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01'
params = {'serviceKey': 'XhzWrdnyXRykvCEJSiPqWWjHuP7u5stjflVUZ81wQeY2mTRWNLloRMZsBTeiViMmiCjFw1xAxUfKf5FyXJaxuQ==',
          'item_name': '', 'entp_name': '', 'item_seq': '', 'img_regist_ts': '', 'pageNo': '1', 'numOfRows': '3',
          'edi_code': '642101571', 'type': 'json'}

response = requests.get(url, params=params).json()

print(response)

# A = [{'color': 'green', 'shape': 'circle'}, {'color': 'blue', 'shape': 'rectangle'}, {'color': 'white', 'shape': 'circle'}]
# B = [{'color': 'blue', 'shape': 'rectangle'}, {'color': 'white', 'shape': 'circle'}]
# result = all(elem in A  for elem in B)
# print(result)
#
# print(PillData.objects.first())
