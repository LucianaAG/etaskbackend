from datetime import datetime
from django.contrib.sessions.models import Session
from django.http import QueryDict
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from user.authentication_mixins import Authentication
from user.serializers import UserSerializer, UserTokenSerializer, RegisterUserSerializer


class Register(GenericAPIView):
    """
       Esta clase tiene una funcion que se encarga de procesar el metodo
       'post' básico.   
    
    """
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Utils():
    """
      La clase contiene una funcion que se encarga de filtrar según la fecha actual las sesiones creadas y
      almacenarlas en 'all_sessions'. Evalua si la variable contiene algo y de ser así, itera a través de
      su contenido y cambia la codificación de los elementos. Por último evalua si el 'id' relacionado al
      usuario es de tipo entero y elimina la sesion.
    
    """
    @staticmethod
    def delete_sessions(user):
        all_sessions = Session.objects.filter(expire_date = datetime.now())
        if all_sessions.exists():
            for session in all_sessions:
                session_data = session.get_decoded()
                if user.id == int(session_data.get('_auth_user_id')):   
                    session.delete()


class Login(ObtainAuthToken, Utils):

    def post(self, request, *args, **kwargs):
        """
           Se extrae el username, email y password para almacernarlos en un diccionario.
           Luego se crea un diccionario de tipo 'QueryDict' al que se le asigna el contenido
           de 'ordinary_dict' y este se pasa al serializador. Se evalua la validación del seriali
           ser y si resulta en positivo, se le asigna a una variable el valor de 'user' contenido
           en el serializer, si no, se notifica un error. Luego se evalua si ese user contenido en la variable está activo
           y si resulta en que sí, se crea un token y se lo relaciona con ese usuario.
        
        """
        ordinary_dict = {'username': request.data['email'], 'password': request.data['password'], }
        query_dict = QueryDict('', mutable=True)
        query_dict.update(ordinary_dict)

        login_serializer = self.serializer_class(
            data = query_dict,
            context = {'request': request}
        )

        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']

            token, created = Token.objects.get_or_create(user = user)
            user_serializer = UserSerializer(user)

            if created:
                return Response({
                    'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Successful login.',
                        }, status = status.HTTP_200_OK)
            else:
                    self.delete_sessions(user)
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Successful login.',
                        }, status = status.HTTP_200_OK)
        else:
            return Response({'error':'[!] Incorrect email or password.'}, status = status.HTTP_400_BAD_REQUEST)
        

class Logout(Authentication, APIView, Utils):

    def post(self, request, *args, **kwargs):
        """
          Se obtiene el campo user y se lo almacena en una variable, luego a la variable 'token'
          se le asigna el token autenticado. Se evalua que el token exista, si es así, se asigna
          a 'user' el token asociado al usuario, se llama a la funcion 'delete_sessions' y se le pasa
          la variable que contiene el token asociado al usuario y lo elimina, luego se notifica al usuario
          que su sesion ha sido elimina y su token también.
        
        """
        try:
            
            user = request.GET.get('user')

            token = Token.objects.get(user=self.user)

            if token:

                user = token.user
                self.delete_sessions(user)
                token.delete()
                session_message = '[*] User sessions for {} deleted.'.format(user)
                token_message = '[*] Token deleted.'
                return Response({
                    'token_message': token_message,
                    'session_message': session_message
                }, status=status.HTTP_200_OK)
            
            return Response({'error':'[!] User with those credentials not found.'}, status = status.HTTP_400_BAD_REQUEST)

        except Token.DoesNotExist:
            return Response({'error':'[!] Token not found in the request.'}, status = status.HTTP_409_CONFLICT)


