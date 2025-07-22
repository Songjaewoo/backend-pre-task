from django.db import models


class Contact(models.Model):
    profile_image_url = models.URLField(max_length=255, blank=True, default='')
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=30, blank=True, default='')
    company = models.CharField(max_length=100, blank=True, default='')
    job_title = models.CharField(max_length=100, blank=True, default='')
    memo = models.TextField(blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    birthday = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, default='')

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='labels')

    class Meta:
        db_table = 'label'

    def __str__(self):
        return self.name


