from django.contrib import admin
# from university_project.admin_site import custom_admin_site
# Register your models here.
from .models import Department, DepartmentImages


class DepartmentInline(admin.TabularInline):
    model = DepartmentImages

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [
        DepartmentInline,
    ]
