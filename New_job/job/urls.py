from django.urls import path, include
from django.contrib import admin
from job import views

urlpatterns = [
    path('postjob/',views.JobPostView.as_view()),
    path('myposts/',views.MyPostsView.as_view()),
    path('listjob/', views.JobListView.as_view()),
    path('filterjob/', views.JobFiltersView.as_view()),
    path('applyjob/', views.JobApplyView.as_view()),
    path('appliedjobs/', views.JobAppliedView.as_view()),
    path('updatejob/<pk>', views.JobUpdateDeleteView.as_view()),
    path('viewprofile/<applicant_id>', views.ViewProfileView.as_view()),
    path('jobstatus/<job_id>', views.JobStatusView.as_view())
]
