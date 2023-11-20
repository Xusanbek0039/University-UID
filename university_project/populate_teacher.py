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

teacher_rank = [
    "Lecturer",
    "Assistant professor",
    "Associate professor",
    "Professor",
    "Professor emeritus",
]

pictures = [
    'teachers/te2.jpg', 'teachers/te3.jpg', 'teachers/te3.jfif',
    'teachers/te4.jpg', 'teachers/te1.png', 'teachers/te5.png',
    'teachers/te6.png', 'teachers/te7.png', 'teachers/te8.jfif',
]

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

        fake_department = Department.objects.get(name='FISHERIES AND MARINE SCIENCE')

        path = random.choice(pictures)
        # profile_pic = os.path.join()
        Teacher_ID = str("teacher10100")+str(count)
        portfolio_site = fakegen.url()
        count=count + 1

        teacher = Teacher.objects.get_or_create(user=user, department=fake_department,
                profile_pic=path, Teacher_ID=Teacher_ID,
                portfolio_site=portfolio_site, academic_rank=random.choice(teacher_rank))[0]



if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    populate(10)
    print('Populating Complete')









#
