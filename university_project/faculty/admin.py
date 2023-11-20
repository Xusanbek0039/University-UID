from django.contrib import admin

# Register your models here.
from .models import Faculty, FacultyImages, VarsityImages

class FacultyImageInline(admin.TabularInline):
    model = FacultyImages

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    inlines =[
        FacultyImageInline,
    ]

admin.site.register(VarsityImages)
