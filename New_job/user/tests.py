from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.utils import json


def create_admin(**params):
    return get_user_model().objects.create_admin(**params)


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestCase(APITestCase):


    def setUp(self):
        self.client = APIClient()


    def test_recruiter_signup(self):
        payload = {'name': 'recruiter', 'designation': 'HR', 'company': 'ABC Tech Solutions', 'email': 'recruiter@xyz.com',
                   'date_of_birth': '1980-01-01', 'gender': 'Male', 'mobile_number': 9111111111,
                   'about_company': 'ABC Tech Solutions was established in 1990 to provides technology and consulting services',
                   'website': 'https://www.abctech.com/' ,'password': 'Pass@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'Your account has been created successfully'})


        payload = {'name': 'testrecruiter2', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@xyz.com',
                   'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9222222222,
                   'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                   'website': 'https://www.itservices.com/' ,'password': 'Word@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'name': ['Enter a valid name']})


        payload = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@.com',
                   'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9222222222,
                   'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                   'website': 'https://www.itservices.com/' ,'password': 'Word@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')

        self.assertJSONEqual(response_content, {'email': ['Enter a valid email']})


        payload = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'recruiter@xyz.com',
                   'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9222222222,
                   'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                   'website': 'https://www.itservices.com/' ,'password': 'Word@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'email': ['user details with this email already exists.']})


        payload = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@xyz.com',
                   'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 1234567,
                   'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                   'website': 'https://www.itservices.com/' ,'password': 'Word@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'mobile_number': ['Enter a valid number']})


        payload = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@xyz.com',
                   'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9111111111,
                   'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                   'website': 'https://www.itservices.com/' ,'password': 'Word@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'mobile_number': ['user details with this mobile number already exists.']})


        payload = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@xyz.com',
                   'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9222222222,
                   'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                   'website': 'https://www.itservices.com/' ,'password': 'word'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'password': ['Enter a valid password']})


        payload = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@xyz.com',
                   'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9222222222,
                   'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                   'website': 'https://www.itservices.com/' ,'password': 'Word@123'}
        response = self.client.post('/recruiter/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'Your account has been created successfully'})

    def test_seeker_user(self):
        payload = {'name': 'seeker', 'email': 'seeker@abc.com', 'date_of_birth': '1995-01-01', 'gender': 'Male', 'mobile_number': 8111111111,
                   'address': 'Chennai, Tamilnadu', 'password': 'Test@456', 'course': 'MBA', 'specialization': 'Marketing and Finance',
                   'course_type': 'Part-time', 'college': 'Anna University', 'percentage': '78', 'year_of_passing': '2018', 'skills': 'Marketing, Financial reporting, Analytical ability',
                   'summary': 'To achieve the objectives of the company with honesty and fairness and to continuously upgrade my knowledge and skills.',
                   'experience_level': 'Experienced', 'designation': 'Marketing Analyst',
                   'responsibilities': 'Tracking advertising costs, researching consumer behavior and exploring market trends and opportunities.',
                   'company': 'Branded Marketing', 'location': 'Chennai', 'worked_from': '2018-06-01', 'to': '2020-01-01'}
        response = self.client.post('/seeker/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'Your account has been created successfully'})


        payload = {'name': 'testseeker25', 'email': 'testseeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8222222222,
                   'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
                   'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                   'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                   'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}
        response = self.client.post('/seeker/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')

        self.assertJSONEqual(response_content, {'name': ['Enter a valid name']})


        payload = {'name': 'testseeker', 'email': 'testseeker@abc', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8222222222,
                   'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
                   'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                   'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                   'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}
        response = self.client.post('/seeker/signup/', data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'email': ['Enter a valid email']})


        payload = {'name': 'testseeker', 'email': 'seeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8222222222,
                   'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
                   'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                   'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                   'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}
        response = self.client.post('/seeker/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'email': ['user details with this email already exists.']})


        payload = {'name': 'testseeker', 'email': 'testseeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 67890,
                   'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
                   'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                   'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                   'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}
        response = self.client.post('/seeker/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'mobile_number': ['Enter a valid number']})


        payload = {'name': 'testseeker', 'email': 'testseeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8111111111,
                   'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
                   'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                   'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                   'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}
        response = self.client.post('/seeker/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'mobile_number': ['user details with this mobile number already exists.']})


        payload = {'name': 'testseeker', 'email': 'testseeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8222222222,
                   'address': 'Bengaluru, Karnataka', 'password': 'demo', 'course': 'B.E', 'specialization': 'IT',
                   'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                   'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                   'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}
        response = self.client.post('/seeker/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'password': ['Enter a valid password']})


        payload = {'name': 'testseeker', 'email': 'testseeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8222222222,
                   'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
                   'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                   'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                   'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}
        response = self.client.post('/seeker/signup/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'Your account has been created successfully'})

    # initialize payloads
    recruiter = {'name': 'recruiter', 'designation': 'HR', 'company': 'ABC Tech Solutions', 'email': 'recruiter@xyz.com',
                 'date_of_birth': '1980-01-01', 'gender': 'Male', 'mobile_number': 9111111111,
                 'about_company': 'ABC Tech Solutions was established in 1990 to provides technology and consulting services',
                 'website': 'https://www.abctech.com/' ,'password': 'Pass@123'}

    testrecruiter = {'name': 'testrecruiter', 'designation': 'Project Manager', 'company': 'IT Services', 'email': 'testrecruiter@xyz.com',
                     'date_of_birth': '1975-01-01', 'gender': 'Female', 'mobile_number': 9222222222,
                     'about_company': 'IT Services was established in 2010 to provide digital, software and operations services',
                     'website': 'https://www.itservices.com/' ,'password': 'Word@123'}

    seeker = {'name': 'seeker', 'email': 'seeker@abc.com', 'date_of_birth': '1995-01-01', 'gender': 'Male', 'mobile_number': 8111111111,
              'address': 'Chennai, Tamilnadu', 'password': 'Test@456', 'course': 'MBA', 'specialization': 'Marketing and Finance',
              'course_type': 'Part-time', 'college': 'Anna University', 'percentage': '78', 'year_of_passing': '2018', 'skills': 'Marketing, Financial reporting, Analytical ability',
              'summary': 'To achieve the objectives of the company with honesty and fairness and to continuously upgrade my knowledge and skills.',
              'experience_level': 'Experienced', 'designation': 'Marketing Analyst',
              'responsibilities': 'Tracking advertising costs, researching consumer behavior and exploring market trends and opportunities.',
              'company': 'Branded Marketing', 'location': 'Chennai', 'worked_from': '2018-06-01', 'to': '2020-01-01'}

    testseeker = {'name': 'testseeker', 'email': 'testseeker@abc.com', 'date_of_birth': '1999-12-01', 'gender': 'Female', 'mobile_number': 8222222222,
                  'address': 'Bengaluru, Karnataka', 'password': 'Demo@456', 'course': 'B.E', 'specialization': 'IT',
                  'course_type': 'Full-time', 'college': 'Bangalore University', 'percentage': '80', 'year_of_passing': '2020', 'skills': 'C, C++, Java, Python',
                  'summary': 'To be a successful professional in a globally respected company', 'experience_level': 'Fresher',
                  'designation': '', 'responsibilities': '', 'company': '', 'location': '', 'worked_from': None, 'to': None}

    def test_login(self):
        create_admin(**TestCase.testrecruiter)

        create_user(**TestCase.testseeker)

        # login recruiter
        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        # login seeker with invalid details
        payload = {'email': 'testseeker@abc.com', 'password': 'Demo456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"non_field_errors": ["Unable to authenticate with provided credentials"]})

        # login seeker
        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_access_profile_with_invalid_token(self):
        create_admin(**TestCase.testrecruiter)

        create_user(**TestCase.testseeker)

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # try to view profile without token
        self.client.credentials()
        response = self.client.get('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail": "Authentication credentials were not provided."})


        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # try to view profile with Invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token zzz')
        response = self.client.get('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail': 'Invalid token.'})

    def test_recruiter_profile_view(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # view profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"name": "testrecruiter", "designation": "Project Manager", "company": "IT Services",
        "email": "testrecruiter@xyz.com", "date_of_birth": "1975-01-01", "gender":"Female", "mobile_number": 9222222222,
        "about_company": "IT Services was established in 2010 to provide digital, software and operations services", "website":"https://www.itservices.com/"})

    def test_update_recruiter_profile(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # update profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'mobile_number': 9222222220}
        response = self.client.patch('/recruiterprofile/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"name": "testrecruiter", "designation": "Project Manager", "company": "IT Services",
        "email": "testrecruiter@xyz.com", "date_of_birth": "1975-01-01", "gender":"Female", "mobile_number": 9222222220,
        "about_company": "IT Services was established in 2010 to provide digital, software and operations services", "website":"https://www.itservices.com/"})


    def test_delete_recruiter_profile(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # delete profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_seeker_profile_view(self):
        create_user(**TestCase.testseeker)

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # view profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"name": "testseeker", "email": "testseeker@abc.com", "date_of_birth": "1999-12-01",
        "gender": "Female", "mobile_number": 8222222222, "address": "Bengaluru, Karnataka", "course": "B.E", "specialization": "IT",
        "course_type": "Full-time", "college": "Bangalore University", "percentage": "80.00", "year_of_passing": 2020, "skills": "C, C++, Java, Python",
        "summary": "To be a successful professional in a globally respected company", "experience_level": "Fresher", "designation":"",
        "responsibilities": "", "company": "", "location": "", "worked_from": None, "to": None})


    def test_update_seeker_profile(self):
        create_user(**TestCase.testseeker)

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # update profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'skills': 'C, C++, Java, Python, SQL'}
        response = self.client.patch('/seekerprofile/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"name": "testseeker", "email": "testseeker@abc.com", "date_of_birth": "1999-12-01",
        "gender": "Female", "mobile_number": 8222222222, "address": "Bengaluru, Karnataka", "course": "B.E", "specialization": "IT",
        "course_type": "Full-time", "college": "Bangalore University", "percentage": "80.00", "year_of_passing": 2020, "skills": "C, C++, Java, Python, SQL",
        "summary": "To be a successful professional in a globally respected company", "experience_level": "Fresher", "designation":"",
        "responsibilities": "", "company": "", "location": "", "worked_from": None, "to": None})


    def test_delete_seeker_profile(self):
        create_user(**TestCase.testseeker)

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # delete profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_recruiter_logout(self):
        create_admin(**TestCase.testrecruiter)

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message": "You've been logged out successfully"})

        # try to view profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail": "Invalid token."})

        # try to update profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'mobile_number': 9222222220}
        response = self.client.patch('/recruiterprofile/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail": "Invalid token."})

        # try to delete profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/recruiterprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_seeker_logout(self):
        create_user(**TestCase.testseeker)

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message": "You've been logged out successfully"})

        # try to view profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail": "Invalid token."})

        # try to update profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'skills': 'C, C++, Java, Python, SQL'}
        response = self.client.patch('/seekerprofile/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail": "Invalid token."})

        # try to delete profile after logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/seekerprofile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
