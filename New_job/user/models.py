from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError(('email is must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, **kwargs):
        return self._create_user(is_staff=False, is_superuser=False,**kwargs)

    def create_admin(self, **kwargs):
        return self._create_user(is_staff=True, is_superuser=False, **kwargs)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save()
        return user

MOBILE_REGEX= RegexValidator(r'^[7,8,9][0-9]{9}$',['Enter a valid number'])
EMAIL_REGEX = RegexValidator(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$',['Enter a valid email'])
NAME_REGEX = RegexValidator(r'^[A-Za-z]{4,}$',['Enter a valid name'])

class UserDetails(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=250, unique=True, validators=[EMAIL_REGEX,])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True, validators=[NAME_REGEX,])
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=240, null=True)
    mobile_number = models.IntegerField(unique=True, null=True, validators=[MOBILE_REGEX,])
    address = models.TextField()
    course = models.CharField(max_length=240)
    specialization = models.CharField(max_length=240)
    course_type = models.CharField(max_length=240)
    college = models.CharField(max_length=240)
    percentage= models.DecimalField(max_digits=4 , decimal_places=2, null=True)
    year_of_passing = models.IntegerField(null=True)
    skills = models.CharField(max_length=240, null=True)
    summary = models.TextField(null=True)
    experience_level= models.CharField(max_length=240, null=True)
    designation = models.CharField(max_length=240, null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=240, null=True, blank=True)
    location= models.CharField(max_length=240,null=True, blank=True)
    worked_from = models.DateField(null=True)
    to = models.DateField(null=True)
    about_company = models.TextField(null=True)
    website =models.URLField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','mobile_number']

    def __str__(self):
        return self.email
