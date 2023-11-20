from django.shortcuts import render, get_object_or_404, redirect
# Extra Imports for the Login and Logout Capabilities
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from PIL import Image
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin
from django.template import context
from django.contrib.auth.forms import PasswordChangeForm

from django.views.generic import (TemplateView,ListView,View,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory

from . models import Faculty, FacultyImages
from . forms import FacultyForm, FacultyImageForm



class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser



@login_required
def CreateFaculty(request):
    if request.user.is_superuser:
        ImageFormSet = modelformset_factory(model=FacultyImages,
                                    form=FacultyImageForm, extra=3 )

        if request.method == 'POST':
            facultyForm = FacultyForm(request.POST)
            formset = ImageFormSet(request.POST, request.FILES,
                                queryset=FacultyImages.objects.none())

            if facultyForm.is_valid() and formset.is_valid():
                faculty_form = facultyForm.save(commit=False)
                faculty_form.user = request.user
                faculty_form.save()

                # faculty_form = faculty_form.cleaned_data()
                name = request.POST.get('name')
                from django.utils.text import slugify
                faculty_slug = slugify(name)

                for form in formset.cleaned_data:
                    #this helps to not crash if the user
                    #do not upload all the photos
                    if form:
                        image = form['image']
                        faculty_image = FacultyImages(faculty=faculty_form, image=image)
                        faculty_image.save()

                messages.success(request,
                            "Photos has been uploaded to faculties section of media!")
                return HttpResponseRedirect(reverse("faculties:faculty_detail", kwargs={"faculty_slug":faculty_slug}))
            else:
                print(facultyForm.errors, formset.errors)
        else:
            facultyForm = FacultyForm()
            formset = ImageFormSet(queryset=FacultyImages.objects.none())
        return render(request, 'faculties/faculty_form.html', {
                                "faculty_form":facultyForm,
                                "formset":formset
                            })
    else:
        return HttpResponse("You must be a superuser to create a faculty!")



class UpdateFaculty(SuperUserCheck, UpdateView):
    redirect_field_name = 'faculties/faculty_list.html'

    form_class = FacultyForm
    model = Faculty
    slug_field = 'faculty_slug'
    slug_url_kwarg = 'faculty_slug'

    template_name = 'faculties/faculty_update.html'


class FacultyList(ListView):
    model = Faculty
    template_name = 'faculties/faculty_list.html'


class FacultyDetail(DetailView):
    model = Faculty
    slug_field = 'faculty_slug'
    slug_url_kwarg = 'faculty_slug'
    template_name='faculties/faculty_detail.html'


class FacultyDelete(SuperUserCheck, DeleteView):
    success_url = reverse_lazy('faculties:faculty_list')
    model = Faculty
    slug_field = 'faculty_slug'
    slug_url_kwarg = 'faculty_slug'

    template_name='faculties/faculty_confirm_delete.html'


from . models import VarsityImages
from . forms import VarsityImageForm
@login_required
def facutyimages(request):
    ImageFormSet = modelformset_factory(model=VarsityImages,
                form=VarsityImageForm, extra=7)

    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES,
                                queryset=VarsityImages.objects.none())

        if formset.is_valid():
            formset.save()
            messages.success(request,
                            "Photos has been uploaded to faculties section of media!")
            return HttpResponseRedirect(reverse("faculties:varsity_images"))
        else:
            print(facultyForm.errors, formset.errors)
    else:
        formset = ImageFormSet(queryset=FacultyImages.objects.none())

    return render(request, 'faculties/gallery_form.html', {
                                "formset":formset
                            })


class ImageList(ListView):
    model = VarsityImages
    context_object_name = 'varsity_images'

    template_name = 'faculties/gallery.html'
