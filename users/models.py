from django.db import models

# Create your models here.

class User(models.Model):
    userId = models.CharField(max_length=20)
    userPassword = models.CharField(max_length=20)
    userRealName = models.CharField(max_length=10)
    userEmail = models.EmailField(max_length=30)

# 사용자의 처방건 일렬번호
class Presc(models.Model):
    prescNo = models.DecimalField(max_digits=13, decimal_places=0)