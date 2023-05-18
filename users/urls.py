from django.urls import path
from . import views
from .views import RegisterView

urlpatterns = [
    path('', views.index),
    path('user/', views.UserView.as_view()),
    path('prescription/', views.PrescriptionView.as_view()),
    path('druginfo/', views.DrugInfoView.as_view()),
   path('register/', RegisterView.as_view()),
    # path('schedules/', views.scheduleList),
]