from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User

# to make tests success just uncomment urls in auth/urls.py

# ************** Test Cases ***********************
class BaseTest(TestCase):
    def setUp(self):
        self.client =Client()
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.issue_url = reverse('issue')
        self.resetPassword_url = reverse('resetPassword')
        self.user={
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'password',
            'password2':'password'
        }
        self.user_short_password={
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'tes',
            'password2':'tes'
        }

        self.user_unmatching_password={

            'email':'testemail@gmail.com',
            'username':'username',
            'password':'teslatt',
            'password2':'teslatto'
                    }

        self.user_invalid_email={
            
            'email':'test.com',
            'username':'username',
            'password':'teslatt',
            'password2':'teslatto' }

        self.not_valid_issue_date = {
            'isbn' :"123",
            'username' :'user1',
            'issue_date' : '05/01/2021',
            'issue_for' : '04/01/2021'
        }

        self.issue_with_empty_issue_date = {
            'isbn': "123",
            'username': 'user1',
            'issue_date': '',
            'issue_for': '04/01/2021'
        }

        self.issue_with_empty_issue_for = {
            'isbn': "123",
            'username': 'user1',
            'issue_date': '05/01/2021',
            'issue_for': ''
        }

        self.issue_with_empty_dates = {
            'isbn': "123",
            'username': 'user1',
            'issue_date': '',
            'issue_for': ''
        }

        self.not_found_email_for_reset_password ={
            'email':'shrooq@gmail.com'
        }
        self.not_email_for_reset_password ={
            'email':'shrooq'
        }
        self.weak_password ={
            'password': '123456789',
            'password2':'123456789'
        }

        self.not_matching_passwords ={
            'password': 'newpassword',
            'password2': 'newpasswo'
        }
        self.empty_passwords ={
            'password': '',
            'password2': ''
        }

        self.empty_password = {
            'password': '',
            'password2': 'newpassword'
        }
        self.empty_password2 = {
            'password': 'newpassword',
            'password2': ''
        }
   
        return super().setUp()


#*************Register units test****************
class RegisterTest(BaseTest):
   def test_can_view_page_correctly(self):
       response=self.client.get(self.register_url)
       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'auth/register.html')

   def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

   def test_cant_register_user_withshortpassword(self):
        response=self.client.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,200)

   def test_cant_register_user_with_unmatching_passwords(self):
        response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
        self.assertEqual(response.status_code,200)

   def test_cant_register_user_with_invalid_email(self):
        response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
        self.assertEqual(response.status_code,200)

   def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,200)

#*************Login units test****************
class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'auth/login.html')

    def test_login_success(self):
        self.client.post(self.register_url,self.user,format='text/html')
        user= User.objects.filter(email=self.user['email']).first()
        user.is_active=True
        user.save()
        response= self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)
        
    def test_cantlogin_with_unverified_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response= self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cantlogin_with_no_username(self):
        response= self.client.post(self.login_url,{'password':'passwped','username':''},format='text/html')
        self.assertEqual(response.status_code,401)

    def test_cantlogin_with_no_password(self):
        response= self.client.post(self.login_url,{'username':'passwped','password':''},format='text/html')
        self.assertEqual(response.status_code,401)

#*************Issue units test****************
class Issue(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.issue_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/issue.html')
    
    def test_not_valid_issue_date(self):
        response = self.client.post(
            self.issue_url, self.not_valid_issue_date, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_empty_issue_date(self):
        response = self.client.post(
            self.issue_url, self.issue_with_empty_issue_date, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_empty_issue_for(self):
        response = self.client.post(
            self.issue_url, self.issue_with_empty_issue_for, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_empty_dates(self):
        response = self.client.post(
            self.issue_url, self.issue_with_empty_dates, format='text/html')
        self.assertEqual(response.status_code, 200)

#*************ResetPassword units test****************
class resetPassword(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.resetPassword_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/resetPassword.html')
     
    def test_empty_passwords(self):
        response = self.client.post(
            self.resetPassword_url, self.empty_password2, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_empty_password(self):
        response = self.client.post(
            self.resetPassword_url, self.empty_password, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_empty_password2(self):
        response = self.client.post(
            self.resetPassword_url, self.empty_password2, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_not_matching_passwords(self):
        response = self.client.post(
            self.resetPassword_url, self.not_matching_passwords, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_weak_password(self):
        response = self.client.post(
            self.resetPassword_url, self.weak_password, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_not_valid_email(self):
        response = self.client.post(
            self.resetPassword_url, self.not_found_email_for_reset_password, format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_not_email(self):
        response = self.client.post(
            self.resetPassword_url, self.not_email_for_reset_password, format='text/html')
        self.assertEqual(response.status_code, 200)

    
