from rest_framework import serializers, status
from user.models import UserDetails
from rest_framework.response import Response
from django.core.validators import RegexValidator

PASSWORD_REGEX = RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$','Enter a valid password')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[PASSWORD_REGEX,])
    class Meta:
        model = UserDetails
        fields=['email','password','name','date_of_birth','gender','mobile_number','address',
                    'course','specialization','course_type','college','percentage',
                    'year_of_passing','skills','summary','experience_level','designation',
                    'responsibilities','company','location','worked_from','to']

    def create(self, validated_data):
        password= validated_data.pop('password')
        user= UserDetails.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class RecruiterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[PASSWORD_REGEX,])
    class Meta:
        model = UserDetails
        fields=['password','name','designation','company','email','date_of_birth','gender','mobile_number','about_company','website']

    def create(self, validated_data):
        password= validated_data.pop('password')
        user= UserDetails.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields=['email','password']
