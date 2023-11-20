from django import forms
from django.contrib.auth.models import User
from .models import Department, DepartmentImages

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'chairman', 'detail', 'faculty', 'established_date')


class DepartmentImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = DepartmentImages
        fields = ('image', )
