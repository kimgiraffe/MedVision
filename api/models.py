from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

# class PersonalInfo():
#     # _apiHost = 'https://api.tilko.net/'
#     # _apiKey = 'd826bc51673f456c960e4b30e2ef08f8'
#
#     # myUserName = None
#     # myBirthDate = None
#     # myUserCellphoneNumber = None
#     # myIdentityNumber = None
#
#     phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
#
#     username = models.CharField(max_length=10)
#     birthdate = models.DateField()
#     cellphoneNo = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True)
#     identityNo = models.CharField(max_length = 13, unique = True)