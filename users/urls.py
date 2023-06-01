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
    # path('schedules/', views.scheduleList),
    path('schedule/<int:presc_id>/delete/', views.ScheduleDeleteView.as_view(), name='delete_schedule'),
    path('schedule/<int:presc_id>/', views.ScheduleUpadateView.as_view(), name='update_schedule'),

    path('user/', views.UserView.as_view()),

]