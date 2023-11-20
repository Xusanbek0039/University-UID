from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
import markdown


class Faculty(models.Model):
    name = models.CharField(max_length=128, unique=True)
    dean = models.CharField(max_length=45, unique=True)
    detail = models.TextField()
    detail_html = models.TextField(editable=False)
    faculty_slug = models.SlugField(allow_unicode=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.faculty_slug = slugify(self.name)
        self.detail_html = markdown.markdown(self.detail)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("faculties:faculty_detail",
                        kwargs={'faculty_slug': self.faculty_slug})

    class Meta:
        ordering = ["name"]


def get_image_filename(instance, filename):
    name = instance.faculty.name
    slug = slugify(name)
    return "faculty_images/%s-%s" % (slug, filename)


class FacultyImages(models.Model):
    faculty = models.ForeignKey(Faculty, related_name='faculty_images', default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='faculty_image', blank=True)


class VarsityImages(models.Model):
    image = models.ImageField(upload_to='university/gallery', blank=True)