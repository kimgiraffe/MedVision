from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.LoginView.as_view(), name='users'),
    path('logout/', views.LogoutView.as_view(), name='users'),
    path('signup/', views.RegisterView.as_view()),
    path('update/', views.UserUpdateView.as_view()),
    path('delete/',views.UserDeleteView.as_view()),
    path('prescription/', views.PrescriptionListView.as_view()),
    path('druginfo/', views.DrugInfoView.as_view()),
    path('prescdetail/', views.PrescDetailListView.as_view()),
    path('schedules/', views.ScheduleListView.as_view()),
    path('forschedule/',views.PrescForScheduleView.as_view()),
    path('maxdoseinfo/',views.ForScheduleDoseView.as_view()),
    path('user/', views.UserView.as_view()),
]