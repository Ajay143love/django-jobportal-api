from django.shortcuts import render
from user.models import UserDetails
from user.serializers import UserSerializer, RecruiterSerializer, AuthTokenSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import mixins, generics, status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class SeekerSignupView( mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes =[]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Your account has been created successfully'}, status=status.HTTP_201_CREATED)
            #return Response(serializer.data, status=status.HTTP_201_CREATED)   #Testing
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterSignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = RecruiterSerializer
    authentication_classes = []
    permission_classes =[]

    def post(self, request):
        serializer = RecruiterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Your account has been created successfully'}, status=status.HTTP_201_CREATED)
            #return Response(serializer.data, status=status.HTTP_201_CREATED)   #Testing
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecruiterProfileView(APIView,mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer = RecruiterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        serializer = RecruiterSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        data=request.data
        user=UserDetails.objects.get(email=request.user)
        user.name=data.get('name',user.name)
        user.company=data.get('company', user.company)
        user.designation=data.get('designation', user.designation)
        user.date_of_birth=data.get('date_of_birth', user.date_of_birth)
        user.gender=data.get('gender', user.gender)
        user.mobile_number=data.get('mobile_number', user.mobile_number)
        user.about_company=data.get('about_company', user.about_company)
        user.website=data.get('website', user.website)
        user.save()
        serializer = RecruiterSerializer(user)
        return Response(serializer.data)


    def delete(self, request):
        user=self.request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeekerProfileView(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        data=request.data
        user=UserDetails.objects.get(email=request.user)
        user.name=data.get('name',user.name)
        user.date_of_birth=data.get('date_of_birth', user.date_of_birth)
        user.mobile_number=data.get('mobile_number', user.mobile_number)
        user.about_company=data.get('about_company', user.about_company)
        user.website=data.get('website', user.website)
        user.gender = data.get('gender',user.gender)
        user.address = data.get('address',user.address)
        user.course = data.get('course',user.course)
        user.specialization = data.get('specialization',user.specialization)
        user.course_type = data.get('course_type',user.course_type)
        user.college = data.get('college',user.college)
        user.percentage = data.get('percentage',user.percentage)
        user.year_of_passing = data.get('year_of_passing',user.year_of_passing)
        user.skills = data.get('skills',user.skills)
        user.company=data.get('company', user.company)
        user.designation=data.get('designation', user.designation)
        user.experience_level = data.get('experience_level',user.experience_level)
        user.summary = data.get('summary',user.summary)
        user.responsibilities = data.get('responsibilities',user.responsibilities)
        user.location = data.get('location',user.location)
        user.worked_from = data.get('summary',user.worked_from)
        user.to = data.get('to',user.to)

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def delete(self, request):
        user=self.request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request):
        #serializer = self.serializer_class(data = request.data)
        #print(request.data)
        username=request.data.get('email')
        password=request.data.get('password')
        #print('user')
        #print(username)
        #print(password)
        user = authenticate(username = username, password = password)
        #print(user)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({"non_field_errors": ["Unable to authenticate with provided credentials"]}, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data,
    #                                        context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({'token': token.key}, status_code=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({"message":("You've been logged out successfully")},status=status.HTTP_200_OK)

        except (AttributeError, ObjectDoesNotExist):
            pass
    def get(self, request):
        return self.logout(request)
