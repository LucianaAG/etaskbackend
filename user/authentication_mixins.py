from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import get_authorization_header
from user.authentication import ExpiringTokenAuthentication


class Authentication(object):

    user = None
    user_token_expired = False

    def get_user(self, request):
        """
           Obtenemos de la request el encabezado de autorización.
           Evaluamos si 'token' está conteniendo algo, si resulta que sí,
           se cambia el formato del token, si no se retorna 'None'.
           Se intancia un objeto de tipo 'ExpiringTokenAuthentication' y se
           autentican las credenciales relacionadas al token.
           Evaluamos si 'user' y 'token' contienen algo, si resulta que sí,
           'self.user' pasará a contener el valor de 'user' y luego se retorná ese valor.    
        
        """
        token = get_authorization_header(request).split()

        if token:
            try:
                token = token[1].decode()
                
            except Exception:
                return None
            
            token_expire = ExpiringTokenAuthentication()
            user, token, message, self.user_token_expired = token_expire.authenticate_credentials(token)

            if user != None and token != None:
                self.user = user
                return user

            return message
        
        return None
    

    def dispatch(self, request, *args, **kwargs):
        
        """
            De la request obtenemos el 'user'.
            Se evalua si la variable 'user' contiene un valor,
            si resulta en que sí, se evalua si el tipo de dato que contiene 'user' es str y
            dentro de la variable response se guarda una respuesta indicando error, la expiración del token
            y un codigo de estado. Se selecciona el renderizador para la respuesta, el tipo de formato en que se
            serializará el contenido de la respuesta (y a la siguiente linea no la entiendo), luego se retorna la respuesta.
            (no entiendo las lineas 70 y 71)

        """

        user = self.get_user(request)

        if user is not None:
            if type(user) == str:
                response = Response({'error':user, 'expired': self.user_token_expired}, 
                                                    status=status.HTTP_400_BAD_REQUEST)
                                                    
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response

            if not self.user_token_expired:
                return super().dispatch(request, *args, **kwargs)

        response = Response({'error':'[!] Credentials not provided.', 'expired': self.user_token_expired}, 
                                                                    status=status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response