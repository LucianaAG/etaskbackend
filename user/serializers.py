from rest_framework import serializers
from user.models import User

class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)


class UserSerializer(serializers.ModelSerializer):
    """
       Definimos los campos a serializar.
    
    """

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'date_joined',
            'last_login',
            'is_admin',
            'is_active',
            'is_staff',
            'is_superuser',
        )

    def to_representation(self,instance):
        """
            La funcion retorna un diccionario que contiene 
            los campos de una instancia.
        
        """
        return {
            'id': instance.id,
            'email': instance.email,
            'date_joined': instance.date_joined,
            'last_login': instance.last_login,
            'is_admin': instance.is_admin,
            'is_active': instance.is_active,
            'is_staff': instance.is_staff,
            'is_superuser': instance.is_superuser
        }


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )

    def validate(self, attrs):
        """
           La funcion toma el email, evalua si ese email ya existe/está en uso, y de ser así,
           lanza un mensaje indicando que ese email ya se encuentra en uso, si no, se retorna
           el email ya validado.

        
        """
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        
        return super().validate(attrs)

    def create(self, validated_data):
        """
           Se obtiene el email y el password y se los contiene en una variable a cada una, luego
           con esos datos se crea un objeto de tipo user y por ultimo, se guarda el nuevo usuario y 
           se lo retorna.
        
        """
        email = validated_data.get('email', '')
        password = validated_data.get('password', '')

        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.save()

        return user