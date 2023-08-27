from rest_framework import status
from django.test import TestCase
from user.models import User 


class TestRegister(TestCase):

    def test_post(self):

        response = self.client.post(
        '/register/',
        {
            "email": "dai@gmail.com",
            "password": "dai123",
        },
    )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_invalid_credentials(self):
        
        response = self.client.post(
        '/register/',
        {
            "email": "dai@gmail.com",
            #"password": "dai123",
        },
    )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLogin(TestCase):


    def test_post_user_does_not_exist(self):

        response = self.client.post(
            '/login/',
            {
                "email": "pipu@gmail.com",
                "password": "potuelo"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_user_already_logged_in(self):
        response = self.client.post(
            '/register/',
            {
                "email": "pipu@gmail.com",
                "password": "potuelo"
            }
        )
        # token refresh
        response = self.client.post(
            '/login/',
            {
                "email": "pipu@gmail.com",
                "password": "potuelo"
            }
        )
        response = self.client.post(
            '/login/',
            {
                "email": "pipu@gmail.com",
                "password": "potuelo"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_banned(self):

        user = User.objects.create_user(
            email = "pipu@gmail.com",
            username = "pipu123",
            password = "potuelo"
        )

        user.is_active = False
        user.save()

        response=self.client.post(
            '/login/',
            {
                "email": "pipu@gmail.com",
                "password": "potuelo"
            }
            #headers =  self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





