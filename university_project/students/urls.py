from django.urls import path, include
from . import views

app_name = 'students'

urlpatterns = [
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name="student_logout"),

    path('change/<int:pk>/password/', views.change_password, name='change_password' ),
    path('<department_slug>/<student_slug>/profile/', views.StudentDetailView.as_view(), name='student_detail'),

    path('department/<department_slug>/students', views.StudentList.as_view(), name='student_list'),
    path('update/profile/student/<student_slug>/', views.AccountEditView.as_view(), name='update_student_profile'),
    path('delete/<department_slug>/student/<student_slug>/', views.StudentDeleteView.as_view(), name='delete_student'),

    path('all/students/', views.all_students.as_view(), name='all_students')
]