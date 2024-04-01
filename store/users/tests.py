from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import UserRegistrationForm
from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):
    
    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Testuser',
            'last_name': 'Testuser',
            'username': 'TestUser',
            'email': 'test@test.com',
            'password1': '123aas#3&*A',
            'password2': '123aas#3&*A',
        }
        
    def test_user_registration_get(self):
        response = self.client.get(self.path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')
        
    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)
        
        #Check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())
        
        #check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        # self.assertEqual(
        #     email_verification.first().expiration.date(),
        #     (now() * timedelta(hours=48)).date()
        # )
        
    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)