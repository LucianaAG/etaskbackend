from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework.authentication import TokenAuthentication

class ExpiringTokenAuthentication(TokenAuthentication):
    expired=False

    def authenticate_credentials(self, key):
        """
            Obtenemos el token asociado al usuario. Si el Token para ese usuario existe,
            pero el usuario está inactivo o fue eliminado, se le mostrará un mensaje de error indicandolo o si el token está expirado,
            se le inidicará también con un mensaje, pero si resulta que no es ninguno de estos casos, 
            se le retornará el usuario su token, un mensaje y el tiempo de expiración del token.

            Return:
                * user      : Instance User that sended request
                * token     : New Token or actual token for user
                * message   : Error message
                * expired   : True if token is alive or False if token is expired
        """
        user, token, message = None, None, None

        try:
            token = self.get_model().objects.select_related('user').get(key=key)
            user = token.user
        except self.get_model().DoesNotExist:
            message = '[!] Invalid Token.'
            self.expired = True

        if token is not None:
            if not token.user.is_active:
                message = '[!] User inactive or deleted.'

            is_expired, token = self.token_expire_handler(token)

            if is_expired:
                message = '[!] Token Expired.'

        return (user, token, message, self.expired)
    

    def expires_in(self, token):
        """
           Se calcula el tiempo de expiracion del token para saber cuanto tiempo falta para que el token expire.

        """
        
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time
    
    def is_token_expired(self, token):
        """
          Se notifica la expiración o no del token.
        
        """
        return self.expires_in(token) < timedelta(seconds=0)
    
    def token_expire_handler(self, token):
        """
           Se comprueba si el token caducó, si resulta que sí, este se elimina y se crea uno nuevo.

        """
        is_expired = self.is_token_expired(token)
        if is_expired:
            self.expired = True
            user = token.user
            token.delete()

            token = self.get_model().objects.create(user=user)

        return is_expired, token
