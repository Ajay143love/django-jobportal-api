from django.shortcuts import render
from django.http import Http404
from job.models import JobDetails, ApplicationDetails
from user.models import UserDetails
from rest_framework import mixins, generics, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from job.serializers import JobSerializer, FilterSerializer, ApplicantSerializer
from user.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
import requests


# Create your views here.
class JobPostView( mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = JobSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated]
    def post(self, request):
        data1=request.data
        #print(request.user)
        user1=UserDetails.objects.get(email=request.user)
        if user1.is_staff:
            data1['company']=user1.company
            data1['about_company']=user1.about_company
            data1['website']=user1.website
            data1['recruiter_id']= user1.id
            #print(data1)
            serializer = self.serializer_class(data=data1)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'job details have been posted successfully'}, status=status.HTTP_201_CREATED)
                #return Response(serializer.data, status=status.HTTP_201_CREATED)   #Testing
            return Response(serializer.errors)
        return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)

class MyPostsView(APIView):
    #queryset = JobDetails.objects.all()
    serializer_class = JobSerializer(many = True)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user1= self.request.user
        #user1=UserDetails.objects.get(email=request.user)
        if user1.is_staff:
            jobs = JobDetails.objects.filter(recruiter_id=user1).values('id','job_title','company','description','experience','work_location','employment_type','qualification','about_company','website','openings','no_of_applicants','application_deadline')
            #print(jobs)
            #serializer = self.serializer_class(jobs)
            return Response(jobs)
        return Response({'message': 'You need recruiter privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)


class JobListView(APIView):
    #queryset = JobDetails.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        jobs= JobDetails.objects.all().values('id','job_title','company','description','experience','work_location','employment_type','qualification','about_company','website','openings','no_of_applicants','application_deadline')
        #print(jobs)
        return Response(jobs)
    # def get(self, request):
    #     user1= self.request.user
    #     #print(jobs)
    #     serializer = self.serializer_class()
    #     return Response(serializer)

class JobFiltersView(generics.ListAPIView):
    queryset = JobDetails.objects.all()
    serializer_class = FilterSerializer
    authentication_classes = []
    permission_classes = []
    filter_backends =[filters.SearchFilter]
    search_fields = ['job_title','work_location','company','description']

class JobApplyView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ApplicantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        D=request.data
        count = ApplicationDetails.objects.filter(job_id=D['job_id'], applicant_id=request.user.id).values()
        #print(count)
        if len(count)==0:
            job=JobDetails.objects.filter(id=D['job_id']).values()
            #print(request.user.id)
            user= UserDetails.objects.filter(email = request.user).values()
            user =list(user)
            job =list(job)
            if user[0]['is_staff'] == False:
                #print(job)
                #print(user)
                data1={}
                data1['job_id'] = job[0]['id']
                data1['job_title'] = job[0]['job_title']
                data1['company'] = job[0]['company']
                data1['applicant_id'] = user[0]['id']
                data1['applicant_name'] = user[0]['name']
                data1['applicant_email'] = user[0]['email']
                #print(data1)
                serializer = self.serializer_class(data=data1)
                if serializer.is_valid():
                    serializer.save()
                    job1=JobDetails.objects.get(id=D['job_id'])
                    job1.no_of_applicants = job1.no_of_applicants +1
                    job1.save()
                    return Response({'message':'You have successfully applied for this job'}, status=status.HTTP_200_OK)
                    #return Response(serializer.data, status=status.HTTP_201_CREATED)   #Testing
                return Response(serializer.errors)
            return Response({'message': 'You need seeker privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message':'You have already applied for this job'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class JobAppliedView(APIView):
    #queryset = JobDetails.objects.all()
    serializer_class = ApplicantSerializer(many = True)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user1= UserDetails.objects.filter(email = request.user).values()
        user1 = list(user1)
        if user1[0]['is_staff']==False:
            applications = ApplicationDetails.objects.filter(applicant_id=request.user).values("job_id", "job_title", "company","applicant_id", "applicant_name", "applicant_email")
            #print(applications)
            #serializer = self.serializer_class(applications)
            return Response(applications)
        return Response({'message': 'You need seeker privileges to perform this action'}, status=status.HTTP_403_FORBIDDEN)

class JobUpdateDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return JobDetails.objects.get(pk=pk)
        #except JobDetails.DoesNotExist:
        except JobDetails.DoesNotExist:
            raise Http404({'detail':'Not Found'})

    def patch(self, request, pk):
        user1 = request.user
        job=self.get_object(pk=pk)
        #print(user)
        #print(job.recruiter_id)
        user= UserDetails.objects.filter(email = request.user).values()
        user =list(user)
        if user[0]['is_staff']:
            #print(job.recruiter_id)
            #print(user)
            #print(job)
            if job.recruiter_id == user1:
                data1=request.data
                data1['recruiter_id']=data1.get('recruiter_id',user[0]['id'])
                data1['about_company'] =data1.get('about_company',job.about_company)
                data1['application_deadline']= data1.get('application_deadline',job.application_deadline)
                data1['company'] = data1.get('company',job.company)
                data1['description']= data1.get('description',job.description)
                data1['employment_type']= data1.get('employment_type',job.employment_type)
                data1['experience'] =data1.get('experience',job.experience)
                data1['job_title'] = data1.get('job_title',job.job_title)
                data1['qualification']= data1.get('qualification',job.qualification)
                data1['work_location']=data1.get('work_location',job.work_location)
                #print(data1)
                serializer = JobSerializer(job, data=data1)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message':'job details have been updated successfully'})
                return Response(serializer.errors)
            return Response({'detail':'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message":"You need recruiter privileges to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        user = request.user
        job=self.get_object(pk=pk)
        # print(user)
        # print(job)
        if job.recruiter_id == user:
            job.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail':'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

class ViewProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return UserDetails.objects.get(pk=pk)
        except UserDetails.DoesNotExist:
            raise Http404({'detail':'Not Found'})

    def get(self, request, applicant_id):
        user2 = self.get_object(pk=request.user.id)
        if user2.is_staff:
            #print(applicant_id)
            user1 = self.get_object(pk=applicant_id)
            #print(user1)
            serializer= UserSerializer(user1)
            return Response(serializer.data)
        return Response({"message":"You need recruiter privileges to perform this action"}, status=status.HTTP_403_FORBIDDEN)


class JobStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return ApplicationDetails.objects.filter(job_id=pk).values("job_id", "job_title", "company","applicant_id", "applicant_name", "applicant_email")
        except ApplicationDetails.DoesNotExist:
            raise Http404({'detail':'Not Found'})

    def get(self, request, job_id):
        #print(job_id)
        job= JobDetails.objects.filter(id=job_id).values()
        #print(job)
        user= UserDetails.objects.filter(email = request.user).values()
        user =list(user)
        job =list(job)
        #print(job)
        if user[0]['is_staff']:
            if(job[0]['recruiter_id_id']==user[0]['id']):
                application = self.get_object(pk=job_id)
                #print(list(application))
                #serializer= ApplicantSerializer(application, many=True)
                #print(serializer.data)
                return Response(list(application))
            return Response({'message':'You do not have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)
        return Response({'message':'You need recruiter privileges to perform this action'},status=status.HTTP_403_FORBIDDEN)
