from django import forms
from django.contrib.auth.models import User
from .models import Faculty, FacultyImages, VarsityImages

class FacultyForm(forms.ModelForm):
    class Meta():
        model = Faculty
        fields = ('name', 'dean', 'detail')


class FacultyImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = FacultyImages
        fields = ('image', )


class VarsityImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = VarsityImages
        fields = ('image',)
