from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import Teacher

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = "teacher"
    fk_name = 'user'

class TeacherAdmin(UserAdmin):
    inlines = (TeacherInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(TeacherAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, TeacherAdmin)


#
# class TeacherProfile(admin.TabularInline):
#     model = Teacher
#
# admin.site.unregister(User)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     inlines =[
#         TeacherProfile,
#     ]
#
#
admin.site.register(Teacher)
