from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    mother = models.CharField(max_length=200, blank=True)
    father = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    siblings = models.TextField(blank=True)
    image = models.ImageField(upload_to="students", blank=True)
    dob = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
