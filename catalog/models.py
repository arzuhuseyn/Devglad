from django.db import models

from devglad.utils.base import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class JobPost(BaseModel):
    REQUIRED_EXPERIENCE = (
        (0, 'No experience required'),
        (1, '1 year'),
        (2, '2 years'),
        (3, '3+ years'),
    )
    title = models.CharField(max_length=255, verbose_name="Title of the job post", help_text='Max limit: 255 char.')
    description = models.TextField(verbose_name="Desc.")
    company = models.ForeignKey("catalog.Company",on_delete=models.SET_NULL, related_name="jobposts", null=True, blank=True, verbose_name="Company")
    is_remote = models.BooleanField(default=True, verbose_name="Is remote friendly?")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salary")
    required_experience = models.IntegerField(choices=REQUIRED_EXPERIENCE, default=0, verbose_name="Required experience")
    tags = models.ManyToManyField(Tag, related_name="jobposts", verbose_name="Tags")
    cover_image = models.ImageField(upload_to='jobposts/cover_images/', null=True, blank=True, verbose_name="Cover image")
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title


class Company(BaseModel):
    representative = models.OneToOneField(
        "catalog.Representative",
        on_delete=models.CASCADE,
        related_name="company",
        null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, verbose_name="Location", help_text='Max limit: 255 char.')
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Representative(BaseModel):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Representative"
        verbose_name_plural = "Representatives"

    def __str__(self):
        return self.name

