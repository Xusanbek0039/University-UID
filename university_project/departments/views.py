from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.views.generic import (TemplateView,ListView,View,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.forms import modelformset_factory
from django.contrib import messages

from . models import DepartmentImages, Department
from faculty.models import Faculty
from . forms import DepartmentForm, DepartmentImageForm
from django.contrib.auth.mixins import UserPassesTestMixin


class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser



@login_required
def CreateDepartment(request):
    ImageFormSet = modelformset_factory(model=DepartmentImages,
                                form=DepartmentImageForm, extra=3 )

    if request.method == 'POST':
        departmentForm = DepartmentForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                            queryset=DepartmentImages.objects.none())

        if departmentForm.is_valid() and formset.is_valid():
            department_form = departmentForm.save(commit=False)
            department_form.user = request.user
            department_form.save()

            dept_name = request.POST.get('name')
            faculty_id=request.POST.get('faculty')
            # get_object_or_404(Group,slug=self.kwargs.get("slug"))
            faculty = get_object_or_404(Faculty, pk=faculty_id)
            from django.utils.text import slugify
            dept_slug = slugify(dept_name)
            faculty_slug = slugify(faculty.name)

            for form in formset.cleaned_data:
                #this helps to not crash if the user
                #do not upload all the photos
                if form:
                    image = form['image']
                    department_image = DepartmentImages(department=department_form, image=image)
                    department_image.save()

            messages.success(request,
                        "Photos has been uploaded to departments section of media!")
            print("\n\n****faculty: {} and dept: {}***/n/n".format(faculty_slug, dept_slug))
            return HttpResponseRedirect(reverse("departments:department_detail", kwargs={"faculty_slug":faculty_slug,
                                                                "department_slug":dept_slug}))
        else:
            print(departmentForm.errors, formset.errors)
    else:
        departmentForm = DepartmentForm()
        formset = ImageFormSet(queryset=DepartmentImages.objects.none())
    return render(request, 'departments/department_form.html', {
                            "department_form":departmentForm,
                            "formset":formset
                        })



class DepartmentDetail(DetailView):
    model = Department

    def get_object(self):
        return get_object_or_404(
            Department,
            department_slug__iexact=self.kwargs['department_slug'],
            # access_key=self.kwargs['access_key'],
        )


class DepartmentStudents(DetailView):
    model = Department
    slug_field = 'department_slug'
    slug_url_kwarg = 'department_slug'
    template_name = 'departments/department_students.html'


class DepartmentTeachers(DetailView):
    model = Department
    slug_field = 'department_slug'
    slug_url_kwarg = 'department_slug'
    template_name = 'departments/department_teachers.html'



class UpdateDepartment(SuperUserCheck, UpdateView):

    # def get_redirect_url(self):
    #     return reverse_lazy("departments:department_detail", kwargs={
    #                     "faculty_slug":self.kwargs['faculty_slug'],
    #                     "department_slug":self.kwargs['department_slug']
    #                             })

    def get_object(self):
        return get_object_or_404(
            Department,
            department_slug__iexact=self.kwargs['department_slug'],
            # access_key=self.kwargs['access_key'],
        )

    model = Department
    fields = ('chairman', 'detail')
    template_name = 'departments/department_update.html'



# class DepartmentList(ListView):
#     model = Department


class DepartmentDelete(SuperUserCheck, DeleteView):
    model = Department

    def get_success_url(self):
          # if you are passing 'slug' from 'urls' to 'DeleteView' for teacher
          # capture that 'slug' as dept_slug and pass it to 'reverse_lazy()' function
          Faculty_slug = self.kwargs['faculty_slug']
          return reverse_lazy('faculties:faculty_detail', kwargs={
                                    'faculty_slug': Faculty_slug,
                                    })

    def get_object(self):
        return get_object_or_404(
            Department,
            department_slug__iexact=self.kwargs['department_slug'],
            # access_key=self.kwargs['access_key'],
        )

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Department Deleted")
        return super().delete(*args, **kwargs)


class AllDepartments(ListView):
    model = Department









###########
