from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    Confirm_Password = forms.CharField(label='confirm your password',widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("Confirm_Password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class StudentProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('student_ID', 'session', 'department', 'profile_pic')
