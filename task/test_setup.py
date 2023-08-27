from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User

class TestSetUp(APITestCase):

    def setUp(self):

        self.login_url = '/login/'

        self.user = User.objects.create_superuser(
            username='dai123',
            email= 'lucy@gmail.com',
            password= 'potuelo'
        )
        response = self.client.post(
            self.login_url,
            {
              'email': 'lucy@gmail.com',
              'password': 'potuelo'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.headers = {'Authorization': 'token {}'.format(self.token)}

        return super().setUp()
    

    def no_admin_mode(self):
        self.user = User.objects.create_user(
            email= 'mila@gmail.com',
            username= 'dai',
            password='potuelo'
        ) 

        response = self.client.post(
            self.login_url,
            {
              "email": "mila@gmail.com",
              "password": "potuelo"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token)

        self.headers = {'Authorization': 'Token {}'.format(self.token)}

    
    def logout(self):
        logout_url = '/logout/'

        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
