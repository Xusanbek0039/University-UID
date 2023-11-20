from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from django.views.generic import (TemplateView,ListView,View,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin


class ErrorTemplateView(TemplateView):

    def get_template_names(self):
        template_name = "error.html"
        return template_name

      

class RegistrationOptionsPage(TemplateView):
    template_name = 'registration_options.html'

class LogoutPage(TemplateView):
    template_name = 'thanks.html'

# class HomePage(TemplateView):
#     template_name = 'index.html'
#


from faculty.models import Faculty
from departments.models import Department
class AllFacultyList(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculties = Faculty.objects.all()
        departments = Department.objects.all()

        context["faculties"] = faculties[:6]
        context["departments"] = departments[:5]
        return context



@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('thanks'))




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            user = get_object_or_404(
                        User,
                        username=username
                    )
            print('Someone tried to login and failed. user: {} pass: {}'.format(user.username, user.password))
            print('He used username: {} and password : {}'.format(username,password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'user_login.html')
