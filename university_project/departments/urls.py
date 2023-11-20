from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "departments"

urlpatterns = [
    path('create/new/', views.CreateDepartment, name='create_department'),
    path('UIC/all/departments/', views.AllDepartments.as_view(), name='all_departments'),
    path('UIC/<faculty_slug>/edit/<department_slug>/', views.UpdateDepartment.as_view(), name='update_department'),
    path('UIC/<faculty_slug>/<department_slug>/', views.DepartmentDetail.as_view(), name='department_detail'),
    path('UIC/<faculty_slug>/department/<department_slug>/delete/', views.DepartmentDelete.as_view(), name='delete_department'),
    path('<department_slug>/students/', views.DepartmentStudents.as_view(), name='department_students'),
    path('<department_slug>/teachers/', views.DepartmentTeachers.as_view(), name='department_teachers'),
]