from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    
    def test_registration(self):
        """
        Ensure users can create accounts
        """
        data = {
            "username": "testcase1",
            "email": "testcase@example.com",
            "password": "NewPassword@123",
            "password2": "NewPassword@123"
        }
        response = self.client.post(reverse('registration_view'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
        
        
    def test_duplicate_registration(self):
        """
        Ensure users can't create multiple accounts with the same username
        """
        data = {
            "username": "testcase1",
            "email": "testcase@example.com",
            "password": "NewPassword@123",
            "password2": "NewPassword@123"
        }
        data2 = {
            "username": "testcase1",
            "email": "testcase2@example.com",
            "password": "NewPassword2@123",
            "password2": "NewPassword2@123"
        }
        response = self.client.post(reverse('registration_view'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        try:
            response = self.client.post(reverse('registration_view'), data2)
            duplicate_username = True
        except:
            duplicate_username = False
            
        self.assertEqual(duplicate_username, False)


class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="NewPassword@123")
        
        
    def test_login(self):
        """
        Ensure users with registered accounts can login
        """
        data = {
            "username": "example",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_logout(self):
        """
        Ensure logged in users can log out
        """
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    