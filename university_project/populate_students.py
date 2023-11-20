import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','university_project.settings')

import django
# Import settings
django.setup()

import random
from faculty.models import Faculty, FacultyImages, VarsityImages
from departments.models import Department, DepartmentImages
from teachers.models import Teacher
from django.contrib.auth.models import User
from students.models import Student

from faker import Faker
fakegen = Faker('en_US')


def populate(N):
    count = 1

    for entry in range(N):
        fake_name = fakegen.name().split()

        fake_username = fake_name[0]
        fake_username = fake_username+str(count)

        fake_email = fakegen.email()
        fake_password = 'thisisuser'
        # fake_password.set_password(fake_password)

        try:
            user = User.objects.get(username=fake_username)
        except User.DoesNotExist:
            user = User.objects.get_or_create(username=fake_username,
                                    email=fake_email, password=fake_password)[0]
            # print(user.password)
            user.set_password(user.password)
            user.save()
            print("after",user.password)

        fake_department = Department.objects.get(name='DEPARTMENT OF ENGLISH')

        path = 'students/dept7.png'
        # profile_pic = os.path.join()
        student_ID = str("ASH160150")+str(count)
        count=count + 1
        session = '2012-13'


        student = Student.objects.get_or_create(user=user, department=fake_department,
                profile_pic=path, student_ID=student_ID,session=session)[0]



if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    populate(25)
    print('Populating Complete')









#
