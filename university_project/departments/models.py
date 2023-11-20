from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
import markdown
from faculty.models import Faculty


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    chairman = models.CharField(max_length=45, unique=True)
    detail = models.TextField()
    detail_html = models.TextField(editable=False)
    department_slug = models.SlugField(allow_unicode=True, unique=True)
    acronyms = models.CharField(max_length=10)
    established_date = models.DateTimeField(blank=False)

    faculty = models.ForeignKey(Faculty, blank=False, related_name="departments", on_delete=models.CASCADE)

    # images = models.ManyToManyField(DepartmentImages, through=...)

    def __str__(self):
        return self.name.upper()

    def save(self, *args, **kwargs):
        self.department_slug = slugify(self.name)
        self.detail_html = markdown.markdown(self.detail)

        self.name = self.name.upper()
        self.acronyms = self.name.replace("&", "").replace("AND", "").replace("OF", "")
        self.acronyms = "".join(ch[0] for ch in self.acronyms.split())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("departments:department_detail",
                       kwargs={"faculty_slug": self.faculty.faculty_slug,
                               "department_slug": self.department_slug})

    class Meta:
        ordering = ["name"]


def get_image_filename(instance, filename):
    name = instance.department.name
    slug = slugify(name)
    return "department_images/%s-%s" % (slug, filename)


class DepartmentImages(models.Model):
    department = models.ForeignKey(Department, related_name='department_images', default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='department_image')