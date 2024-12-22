from django.urls import path
from . import authentication_views,employee_views,attendance_views,views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', authentication_views.register_view, name='register'),
    path('login/', authentication_views.login_view, name='login'),
    path('logout/', authentication_views.logout_view, name='logout'),
    path('employee-form/', login_required(employee_views.employee_form), name='employee_form'),
    path('employee-list/', login_required(employee_views.employee_list_view), name='employee_list'),
    path('employee-update/<int:pk>/',login_required(employee_views.update_employee_view), name='update_employee'),
    path('employee-delete/<int:pk>/', login_required(employee_views.delete_employee_view), name='delete_employee'),
    path('', lambda request: redirect('login/')), 
    path('attendance-upload/',login_required(attendance_views.attendance_upload),name='attendance_upload'),
    # path('base/', views.base, name='base'),
    path('index/',login_required (views.index), name='index'),

]
