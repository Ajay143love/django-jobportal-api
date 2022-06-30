from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.utils import json
from django.contrib.auth import get_user_model


def create_admin(**params):
    return get_user_model().objects.create_admin(**params)


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class JobTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

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


    def test_post_job_without_recruiter_access(self):
        create_user(**JobTestCase.testseeker)

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'You need recruiter privileges to perform this action'})

    def test_post_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})


        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # try to post job without token
        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Authentication credentials were not provided."})

        # try to post job with invalid token
        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token zzz')
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail': 'Invalid token.'})

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})


    def test_myposts_without_recruiter_access(self):
        create_user(**JobTestCase.testseeker)

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/myposts/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You need recruiter privileges to perform this action"})

    def test_myposts(self):
        create_admin(**JobTestCase.recruiter)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time', 'qualification': 'MBA/PGDM in Any Specialization',
                   'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        # myposts
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/myposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{"id": 1, "job_title": "Digital Marketing Executive", "company": "ABC Tech Solutions",
                                                 "description": "We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company."
                                                 "Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.", "experience": "1 - 3 years",
                                                 "work_location": "Chennai", "employment_type": "Full Time", "qualification": "MBA/PGDM in Any Specialization",
                                                 "about_company":"ABC Tech Solutions was established in 1990 to provides technology and consulting services",
                                                 "website": "https://www.abctech.com/", "openings":1, "no_of_applicants":0, "application_deadline":"2020-10-30"}])



    def test_list_and_filter_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        # list job
        response = self.client.get('/listjob/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{"id": 1,"job_title": "Digital Marketing Executive", "company": "ABC Tech Solutions",
        "description": "We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.",
        "experience": "1 - 3 years", "work_location": "Chennai", "employment_type": "Full Time", "qualification": "MBA/PGDM in Any Specialization",
        "about_company": "ABC Tech Solutions was established in 1990 to provides technology and consulting services", "website": "https://www.abctech.com/",
        "openings": 1, "no_of_applicants": 0, "application_deadline": "2020-10-30"},
        {"id": 2, "job_title": "Full Stack Web Developer", "company": "IT Services",
        "description": "We are looking for talented web developer capable of developing highly demanding applications.Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.",
        "experience": "0 - 1 years", "work_location": "Bangalore", "employment_type": "Full Time", "qualification": "B.Tech/B.E. in Any Specialization",
        "about_company": "IT Services was established in 2010 to provide digital, software and operations services", "website": "https://www.itservices.com/",
        "openings": 2, "no_of_applicants": 0, "application_deadline": "2020-10-30"}])

        # filter job by title
        response = self.client.get('/filterjob/?search=Web+Developer')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,[{"id": 2, "job_title": "Full Stack Web Developer", "company": "IT Services",
        "description": "We are looking for talented web developer capable of developing highly demanding applications.Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.",
        "experience": "0 - 1 years", "work_location": "Bangalore", "employment_type": "Full Time", "qualification": "B.Tech/B.E. in Any Specialization",
        "about_company": "IT Services was established in 2010 to provide digital, software and operations services", "website": "https://www.itservices.com/",
        "openings": 2, "no_of_applicants": 0, "application_deadline": "2020-10-30"}])

        # filter job by location
        response = self.client.get('/filterjob/?search=chennai')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{"id": 1,"job_title": "Digital Marketing Executive", "company": "ABC Tech Solutions",
        "description": "We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.",
        "experience": "1 - 3 years", "work_location": "Chennai", "employment_type": "Full Time", "qualification": "MBA/PGDM in Any Specialization",
        "about_company": "ABC Tech Solutions was established in 1990 to provides technology and consulting services", "website": "https://www.abctech.com/",
        "openings": 1, "no_of_applicants": 0, "application_deadline": "2020-10-30"}])

        # filter job by skill
        response = self.client.get('/filterjob/?search=python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{"id": 2, "job_title": "Full Stack Web Developer", "company": "IT Services",
        "description": "We are looking for talented web developer capable of developing highly demanding applications.Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.",
        "experience": "0 - 1 years", "work_location": "Bangalore", "employment_type": "Full Time", "qualification": "B.Tech/B.E. in Any Specialization",
        "about_company": "IT Services was established in 2010 to provide digital, software and operations services", "website": "https://www.itservices.com/",
        "openings": 2, "no_of_applicants": 0, "application_deadline": "2020-10-30"}])

        # filter job by company
        response = self.client.get('/filterjob/?search=ABC+Tech+Solutions')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{"id": 1,"job_title": "Digital Marketing Executive", "company": "ABC Tech Solutions",
        "description": "We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.",
        "experience": "1 - 3 years", "work_location": "Chennai", "employment_type": "Full Time", "qualification": "MBA/PGDM in Any Specialization",
        "about_company": "ABC Tech Solutions was established in 1990 to provides technology and consulting services", "website": "https://www.abctech.com/",
        "openings": 1, "no_of_applicants": 0, "application_deadline": "2020-10-30"}])



    def test_apply_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        # recruiter try to apply job
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You need seeker privileges to perform this action"})

        payload = {'email': 'seeker@abc.com', 'password': 'Test@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # try to apply job without token
        self.client.credentials()
        payload = {'job_id': 1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Authentication credentials were not provided."} )

        # try to apply job with invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token zzz')
        payload = {'job_id': 1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail': 'Invalid token.'})

        # apply job
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You have successfully applied for this job"})

        # try to apply same job again
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You have already applied for this job"})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You have successfully applied for this job"})


    def test_applied_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        # recruiter try to access applied jobs
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/appliedjobs/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You need seeker privileges to perform this action"})

        payload = {'email': 'seeker@abc.com', 'password': 'Test@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 1}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You have successfully applied for this job"})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You have successfully applied for this job"})

        # applied jobs
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/appliedjobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,[{"job_id": 1, "job_title": "Digital Marketing Executive", "company": "ABC Tech Solutions",
                                                "applicant_id": 3, "applicant_name": "seeker", "applicant_email": "seeker@abc.com"},
                                               {"job_id": 2, "job_title": "Full Stack Web Developer", "company": "IT Services",
                                                "applicant_id": 3, "applicant_name": "seeker", "applicant_email": "seeker@abc.com"}])


    def test_job_status_without_recruiter_access(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/jobstatus/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You need recruiter privileges to perform this action"})



    def test_job_status(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})


        payload = {'email': 'seeker@abc.com', 'password': 'Test@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You have successfully applied for this job"})

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {'job_id': 2}
        response = self.client.post('/applyjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You have successfully applied for this job"})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/myposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{"id": 2, "job_title": "Full Stack Web Developer", "company": "IT Services",
        "description": "We are looking for talented web developer capable of developing highly demanding applications.Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.",
        "experience": "0 - 1 years", "work_location": "Bangalore", "employment_type": "Full Time", "qualification": "B.Tech/B.E. in Any Specialization",
        "about_company": "IT Services was established in 2010 to provide digital, software and operations services", "website": "https://www.itservices.com/",
        "openings": 2, "no_of_applicants": 2, "application_deadline": "2020-10-30"}])

        # try to access other recruiters job status
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/jobstatus/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You do not have permission to perform this action"})

        # job status
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/jobstatus/2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, [{"job_id": 2, "job_title": "Full Stack Web Developer", "company": "IT Services",
                                                 "applicant_id": 3, "applicant_name": "seeker", "applicant_email": "seeker@abc.com"},
                                                {"job_id":2, "job_title": "Full Stack Web Developer", "company":"IT Services",
                                                 "applicant_id": 4, "applicant_name": "testseeker", "applicant_email": "testseeker@abc.com"}])


    def test_view_profile_without_recruiter_access(self):
        create_user(**JobTestCase.testseeker)

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/viewprofile/3')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You need recruiter privileges to perform this action"})


    def test_view_profile(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        # view profile
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/viewprofile/4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"name": "testseeker", "email": "testseeker@abc.com", "date_of_birth": "1999-12-01", "gender": "Female",
        "mobile_number": 8222222222, "address": "Bengaluru, Karnataka", "course": "B.E", "specialization": "IT", "course_type": "Full-time",
        "college": "Bangalore University", "percentage": "80.00", "year_of_passing": 2020, "skills": "C, C++, Java, Python",
        "summary": "To be a successful professional in a globally respected company", "experience_level": "Fresher", "designation":"",
        "responsibilities": "", "company": "","location": "", "worked_from": None, "to": None})



    def test_update_and_delete_job_without_recruiter_access(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testseeker@abc.com', 'password': 'Demo@456'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'openings': '1'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/updatejob/2', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"message":"You need recruiter privileges to perform this action"})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/updatejob/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'detail': 'You do not have permission to perform this action.'})




    def test_update_and_delete_job(self):
        create_admin(**JobTestCase.recruiter)

        create_admin(**JobTestCase.testrecruiter)

        create_user(**JobTestCase.seeker)

        create_user(**JobTestCase.testseeker)

        payload = {'email': 'recruiter@xyz.com', 'password': 'Pass@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Digital Marketing Executive', 'description': 'We are looking for a talented Marketing Executive to undertake marketing projects for the benefit of our company.'
                   'Skills: Digital Marketing, Customer Experience, Social Media, Marketing Management.', 'experience': '1 - 3 years', 'work_location': 'Chennai', 'employment_type': 'Full Time',
                   'qualification': 'MBA/PGDM in Any Specialization', 'openings': '1', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'email': 'testrecruiter@xyz.com', 'password': 'Word@123'}
        response = self.client.post('/login/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        response_content = json.loads(response.content.decode('utf-8'))
        token = response_content['token']

        payload = {'job_title': 'Full Stack Web Developer', 'description': 'We are looking for talented web developer capable of developing highly demanding applications.'
                   'Skills: Python, Django, MySQL, React, REST APIs, Angular and MongoDB.', 'experience': '0 - 1 years', 'work_location': 'Bangalore', 'employment_type': 'Full Time',
                   'qualification': 'B.Tech/B.E. in Any Specialization', 'openings': '2', 'application_deadline': '2020-10-30'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/postjob/', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been posted successfully'})

        payload = {'openings': '1'}
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.patch('/updatejob/1', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Authentication credentials were not provided."})

        self.client.credentials(HTTP_AUTHORIZATION='Token zzz')
        response = self.client.delete('/updatejob/1')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail":"Invalid token."})

        payload = {'openings': '1'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/updatejob/5', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content,{"detail": "Not found."})

        # try to update other recruiters job details
        payload = {'openings': '1'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/updatejob/1', data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail": "You do not have permission to perform this action."})

        # update
        payload = {'openings': '1'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/updatejob/2', data=payload, format='json')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {'message': 'job details have been updated successfully'})

        # try to delete other recruiters job details
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/updatejob/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_content = response.content.decode('utf-8')
        self.assertJSONEqual(response_content, {"detail": "You do not have permission to perform this action."})

        # delete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/updatejob/2')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
