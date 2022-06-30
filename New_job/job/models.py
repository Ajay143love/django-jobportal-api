from django.db import models
from user.models import UserDetails
#from django.contrib.auth.models import UserDetails
# from django.contrib.auth import get_user_model
# UserDetails = get_user_model()

# Create your models here.
class JobDetails(models.Model):
    job_title = models.CharField(max_length=240)
    company= models.CharField(max_length=240)
    description = models.TextField()
    experience = models.CharField(max_length=240)
    work_location = models.CharField(max_length=240)
    employment_type =models.CharField(max_length=240)
    qualification = models.CharField(max_length=240)
    about_company = models.TextField()
    website = models.URLField(blank=True)
    openings = models.IntegerField()
    no_of_applicants= models.IntegerField(default=0)
    application_deadline = models.DateField()
    recruiter_id = models.ForeignKey(UserDetails, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.job_title


class ApplicationDetails(models.Model):
    job_id = models.ForeignKey(JobDetails, on_delete= models.CASCADE)
    job_title = models.CharField(max_length=240)
    company= models.CharField(max_length=240)
    applicant_id = models.ForeignKey(UserDetails, on_delete= models.CASCADE)
    applicant_name = models.CharField(max_length=240)
    applicant_email = models.CharField(max_length=240)

    def __str__(self):
        return self.job_title
