from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from authentication.utils import generate_token


class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
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
            'password2':'teslatto'
        }
        return super().setUp()
        
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
        self.assertEqual(response.status_code,400)

   def test_cant_register_user_with_unmatching_passwords(self):
        response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
        self.assertEqual(response.status_code,400)
   def test_cant_register_user_with_invalid_email(self):
        response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
        self.assertEqual(response.status_code,400)

   def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400)