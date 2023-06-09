from django.contrib import admin
from .models import User, Prescription, Schedule, DrugInfo, PrescDetail, DrugHour, PillData

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'userId',
        'userRealName',
        'userEmail',
        'userRegisterDatetime',
    )

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        'prescId',
        'prescDate',
        'dispensary'
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'prescId',
        'startDate',
        'endDate',
    )
    def prescId(self, obj):
        return obj.prescription.prescId
@admin.register(DrugInfo)
class DrugInfoAdmin(admin.ModelAdmin):
    list_display = (
        'drugNo',
        'drugName',
        'drugEffect',
        'component',
        'quantity',
    )
@admin.register(PrescDetail)
class PrescDetailAdmin(admin.ModelAdmin):
    list_display = (
        'prescId',
        'drugInfo',
        'dosagePerOnce',
        'dailyDose',
        'totalDosingDays',
    )
    def prescId(self, obj):
        return obj.prescription.prescId
    def drugInfo(self, obj):
        return obj.drugInfo.drugName

@admin.register(DrugHour)
class DrugHourAdmin(admin.ModelAdmin):
    list_display = (
        'prescId',
        'startDate',
        'drugName',
        'hour',
    )
    def startDate(self, obj):
        return obj.schedule.startDate
    def prescId(self, obj):
        return obj.schedule.prescId
    def drugName(self, obj):
        return obj.prescDetail.drugInfo

@admin.register(PillData)
class PillDataAdmin(admin.ModelAdmin):
    list_display = (
        'drugNo',
        'pillShape',
        'pillColor',
        'pillText',
    )