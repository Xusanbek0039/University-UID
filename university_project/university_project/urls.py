"""university_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from . views import ErrorTemplateView
# from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.AllFacultyList.as_view() , name='index'),

    path('registration/options/', views.RegistrationOptionsPage.as_view(), name='registration_options'),
    path('logout/', views.user_logout, name='logout'),
    path('thanks/', views.LogoutPage.as_view(), name='thanks'),

    path('user/login/', views.user_login, name='user_login'),
    path('faculties/', include("faculty.urls", namespace="faculties")),
    path('departments/', include("departments.urls", namespace='departments')),
    path('students/', include("students.urls", namespace='students')),
    path('teachers/', include("teachers.urls", namespace='teachers')),

    re_path(r"^.*$", ErrorTemplateView.as_view(), name='entry-point'),


]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
