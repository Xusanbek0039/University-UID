from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
import markdown
from departments.models import Department


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    department = models.ForeignKey(Department, related_name="students", blank=False, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='students/profile_pics', blank=True)
    student_ID = models.CharField(max_length=20, unique=True, blank=False)
    student_slug = models.SlugField(allow_unicode=True, unique=True)
    session = models.CharField(max_length=9, blank=False)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.student_slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("students:student_detail",
                        kwargs={'department_slug': self.department.department_slug, "student_slug": self.student_slug})

    class Meta:
        ordering = ["student_ID"]
        unique_together = ["user", "department"]