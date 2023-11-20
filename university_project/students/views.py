from django.shortcuts import render, redirect, get_object_or_404

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.utils.text import slugify
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.views.generic import (TemplateView,ListView,View,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.utils.text import slugify

from .forms import StudentForm, StudentProfileInfoForm
from .models import Student
from departments.models import Department

@login_required
def student_logout(request):
    logout(request)
    return redirect('students:student_login')

def student_register(request):
    registered = False

    if request.method == 'POST':
        student_form = StudentForm(data=request.POST)
        student_profile_form = StudentProfileInfoForm(data=request.POST)

        if student_form.is_valid() and student_profile_form.is_valid():
            # Save User Form to Database
            user = student_form.save()

            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            student_profile = student_profile_form.save(commit=False)
            # Set One to One relationship between
            # StudentForm and StudentProfileInfoForm
            student_profile.user = user

            if 'profile_pic' in request.FILES:
                student_profile.profile_pic = request.FILES['profile_pic']

            # now saving the model
            student_profile.save()
            registered = True

            name = request.POST.get('username')
            dept_id=request.POST.get('department')
            # get_object_or_404(Group,slug=self.kwargs.get("slug"))
            department = get_object_or_404(Department, pk=dept_id)
            from django.utils.text import slugify
            student_slug = slugify(name)
            dept_slug = slugify(department.name)
            # print("\n\n****department: {} and student: {}***/n/n".format(dept_slug, student_slug))

            return HttpResponseRedirect(reverse('students:student_detail', kwargs={'department_slug':dept_slug, 'student_slug':student_slug}))
        else:
            print(student_form.errors, student_profile_form.errors)
    else:
        student_form = StudentForm()
        student_profile_form = StudentProfileInfoForm()

    return render(request, "students/student_registration.html",context={
                    'student_form':student_form,
                    'student_profile_form':student_profile_form,
                    'registered':registered})


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")

        else :
            print('Invalid Username: {} and password: {} is provided'.format(username, password))
            return HttpResponse("Invalid username or password supplied!")
    else:
        return render(request, 'students/login.html',{})


@login_required
def change_password(request):
    if request.mathod == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password is changed!")
            logout(request)
            return redirect('user_login')
        else:
            messages.error(request, "Please provide valid information")
    else:
        form = PasswordChangeForm(request, user)
    return render(request, 'students/change_password.html',{
                            'form':form})


class StudentDetailView(SelectRelatedMixin, DetailView):
    select_related = ("user", "department")
    context_object_name = 'student_detail'
    model = Student
    template_name = 'students/student_detail.html'

    def get_object(self):
        return get_object_or_404(
            Student,
            student_slug=self.kwargs['student_slug']
            # access_key=self.kwargs['access_key'],
        )


class StudentList(SelectRelatedMixin, ListView):
    model = Student
    select_related = ("user", "department")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['slug'] = self.kwargs['slug']
    #     # context['current_month'] = self.current_month
    #     return context

from django.forms import ModelForm
@login_required
def StudentUpdate(request, student_slug):
    object = Student.objects.get(student_slug=student_slug)
    form = ModelForm(instance=object)

    return render(request, 'students/profileupdate_form.html', {'form':form})


from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

class StudentUpdateView(InlineFormSetFactory):
    model = Student
    fields = ['profile_pic','department', 'session']

class AccountEditView(UpdateWithInlinesView):
    model = User
    old_password = []
    old_password.clear()
    fields = ['username', 'email', 'password']
    inlines = [StudentUpdateView,]
    template_name = 'students/profileupdate_form.html'

    def get_object(self):
        user = User.objects.get(pk=self.request.user.pk)
        self.old_password.append(user.password)
        return user

    def get_success_url(self):
        user1 = self.get_object()
        if self.old_password[1] == self.old_password[2]:
            print("no change passsword ",user1.password)
        else:
            user1.set_password(user1.password)

        user1.save()
        user1.student.save()

        self.old_password.clear()

        return get_object_or_404(
                    Student,
                    pk=user1.student.id
                ).get_absolute_url()




class StudentDeleteView(LoginRequiredMixin,SelectRelatedMixin, DeleteView):
    login_url = '/login/options/'
    # redirect_field_name = 'blog/post_detail.html'
    model = Student

    def get_object(self):
        return Student.objects.get(student_slug=self.kwargs['student_slug'])

    def get_success_url(self):
          # if you are passing 'slug' from 'urls' to 'DeleteView' for student
          # capture that 'slug' as dept_slug and pass it to 'reverse_lazy()' function
          dept_slug = self.kwargs['department_slug']
          student = self.get_object()
          user = student.user
          logout(self.request)
          user.delete()
          # self.StudentLogoutView()
          return reverse('departments:department_students', kwargs={
                                    'department_slug': dept_slug,})



class all_students(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'students/all_students.html'
