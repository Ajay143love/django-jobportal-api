from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from job.models import JobDetails, ApplicationDetails

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobDetails
        fields = ['job_title','description','experience','work_location','employment_type','qualification','openings','application_deadline','recruiter_id','company','about_company','website']

    def create(self, validated_data):
        #print(validated_data)
        job_post= JobDetails.objects.create(**validated_data)
        job_post.save()
        return job_post

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model= ApplicationDetails
        fields = ['job_id','job_title','company','applicant_id','applicant_name','applicant_email']

# class JobStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= ApplicationDetails
#         fields = ['job_id','job_title','company','applicant_id','applicant_name','applicant_email']

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobDetails
        fields = ['id','job_title','company','description','experience','work_location','employment_type','qualification','about_company','website','openings','no_of_applicants','application_deadline']
