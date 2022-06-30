from django.urls import path, include
from user import views

urlpatterns = [
    path('seeker/signup/',views.SeekerSignupView.as_view()),
    path('recruiter/signup/',views.RecruiterSignupView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('recruiterprofile/',views.RecruiterProfileView.as_view()),
    path('seekerprofile/',views.SeekerProfileView.as_view()),
    path('logout/',views.LogoutView.as_view())

    ]
