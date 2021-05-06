from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=8, null=True)
    type = models.CharField(max_length=15)

    def _str_(self):
        return self.user.username

class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=8, null=True)
    company = models.CharField(max_length=40, null=True)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20, null=True)
    def _str_(self):
        return self.user.username

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=20)
    salary = models.FloatField(max_length=20)
    image = models.FileField()
    description = models.CharField(max_length=150)
    experience = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    creationdate = models.DateField()
    link=models.CharField(max_length=100,null=True)
    def _str_(self):
        return self.title

class AppliedJobs(models.Model):
    candidate= models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    job= models.ForeignKey(Job, on_delete=models.CASCADE)
    recruiter=models.ForeignKey(Recruiter, on_delete=models.CASCADE,default="")
