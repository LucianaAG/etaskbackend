from datetime import datetime
from rest_framework import status
from django.test import TestCase
from user.serializers import RegisterUserSerializer, UserSerializer
from user.models import User
from rest_framework import serializers


class TestRegisterUserSerializer(TestCase):
     
    def test_validate(self):

    # 1- Creacion de objetos ficticios para pasarle al metodo.
        attrs = {
            'email': 'lucygauto@gmail.com',
            'username': 'lucy'
        }

    # 2- Ejecutar el metodo que vamos a testear y obtener la respuesta.
        serializer = RegisterUserSerializer()
        response = serializer.validate(attrs)

        self.assertTrue(response, attrs)

    def test_validate_invalid_email(self):

        User.objects.create(
            email= 'lucy@gmail.com',
            username= 'lucy@mail.com'
        )

        attrs = {
            'email': 'lucy@gmail.com',
            'username': 'lucy@mail.com'
        }

        serializer = RegisterUserSerializer()

        with self.assertRaises(serializers.ValidationError) as context:
            serializer.validate(attrs)

            # Assert that the error message matches your expectation
            self.assertEqual(context.exception.detail, {'email': ['Email is already in use']})


    def test_create(self):

        validated_data = {
            'email': 'lucy@gmail.com',
            'username': 'lucy@gmail.com',
            'password':'mila123',
        }

        serializer = RegisterUserSerializer()
        response = serializer.create(validated_data)

        self.assertTrue(response, validated_data)

    
class TestUserSerializer(TestCase):
    
    def test_to_representation(self):
        
        instance = User.objects.create(
            id='1',
            email='lucy123@gmail.com',
            date_joined='01-01-2001',
            last_login='02-08-2008',
            is_admin=True,
            is_active=False,
            is_staff=False,
            is_superuser=False
        )

        serializer = UserSerializer()
        response = serializer.to_representation(instance)

        self.assertTrue(response, instance)