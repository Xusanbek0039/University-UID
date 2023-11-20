from django.urls import path
from . import views



app_name = "faculties"


urlpatterns = [
    path('create/new/faculty/', views.CreateFaculty, name='create_faculty'),

    path('UIC/<faculty_slug>/edit/', views.UpdateFaculty.as_view(), name='update_faculty'),

    path('UIC/all/', views.FacultyList.as_view(), name='faculty_list'),
    path('UIC/<faculty_slug>/departments/', views.FacultyDetail.as_view(), name='faculty_detail'),
    path('UIC/<faculty_slug>/delete', views.FacultyDelete.as_view(), name='delete_faculty'),

    path('UIC/form/upload/images', views.facutyimages, name='gallery_form'),
    path('UIC/gallery/', views.ImageList.as_view(), name='varsity_images'),

]
