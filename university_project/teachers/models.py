from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import markdown
from departments.models import Department

teacher_rank = [
    ("Lecturer", "Lecturer"),
    ("Assistant professor", "Assistant professor"),
    ("Associate professor", "Associate professor"),
    ("Professor", "Professor"),
    ("Professor emeritus", "Professor emeritus"),
]

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    department = models.ForeignKey(Department, blank=False, related_name="teachers", on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='teachers/profile_pics', blank=True)
    Teacher_ID = models.CharField(max_length=20, unique=True, blank=False)
    portfolio_site = models.URLField(blank=True)
    academic_rank = models.CharField(blank=False, max_length=100, choices=teacher_rank)
    teacher_slug = models.SlugField(allow_unicode=True, unique=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.teacher_slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("teachers:teacher_detail",
                        kwargs={"department_slug": self.department.department_slug,
                            "teacher_slug": self.teacher_slug})

    class Meta:
        ordering = ["Teacher_ID"]
        unique_together = ["Teacher_ID", "department"]