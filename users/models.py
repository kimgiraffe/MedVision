from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=12, unique=True)
    userPassword = models.CharField(max_length=20)
    userRealName = models.CharField(max_length=10, blank=True, null=False, default="")
    userEmail = models.EmailField(max_length=25)
    userRegisterDatetime = models.DateTimeField(auto_now_add=True)

class Prescription(models.Model):
    userId = models.ForeignKey("User",
                               on_delete = models.CASCADE,
                               db_column="userId",
                               related_name='prescriptions'
                               )
    prescId = models.DecimalField(max_digits=13, decimal_places=0, primary_key=True)
    prescDate = models.DateField(default='')        # 조제일
    dispensary = models.CharField(max_length=15)    # 조제기관

class Schedule(models.Model):
    startDate = models.DateField(default='')    # 시작일
    endDate = models.DateField(default='')      # 종료일
    prescription = models.ForeignKey("Prescription", # 처방번호
                                primary_key=True,
                                on_delete=models.CASCADE,
                                db_column="prescId",
                                related_name='schedules')
class DrugInfo(models.Model):
    drugNo = models.DecimalField(max_digits=9, decimal_places=0, primary_key=True)
    drugName = models.CharField(max_length=25)
    drugEffect = models.CharField(max_length=50)    # 효능
    component = models.CharField(max_length=50)     # 성분
    quantity = models.CharField(max_length=12)      # 함량

class PrescDetail(models.Model):
    prescription = models.ForeignKey("Prescription",  # 처방번호
                                # primary_key=True,
                                on_delete=models.CASCADE,
                                db_column="prescId",
                                related_name='prescDetail')
    drugNo = models.DecimalField(max_digits=9, decimal_places=0)
    dosagePerOnce = models.DecimalField(max_digits=6, decimal_places=2)  # 1회 투약량
    dailyDose = models.IntegerField()           # 1일 투여횟수
    totalDosingDays = models.IntegerField()     # 총 투여일수

class DrugHour(models.Model):
    schedule = models.ForeignKey("Schedule",
                                   on_delete=models.CASCADE,
                                   db_column="scheduleId",
                                   related_name="drugHour")
    drugNo = models.DecimalField(max_digits=9, decimal_places=0)
    hour = models.TimeField()

class PillData(models.Model):
    drugNo = models.DecimalField(max_digits=9, decimal_places=0, primary_key=True)
    pillShape = models.TextField(max_length=6)
    pillColor = models.TextField(max_length=20)
    pillText = models.TextField(max_length=30, null=True)
