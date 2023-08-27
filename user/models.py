from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from notifications.models import Subscriber
from notifications.models import Notification
from datetime import datetime

from simple_history.models import HistoricalRecords

class MyUserManager(BaseUserManager):

    """

       Definimos la clase MyUserManager, la cual maneja una funcion para crear usuario y super usuario.
       La funcion 'Create_user' evalua que exista el email y el username.
       normaliza el email para que cumpla con los requisitos, guarda la contraseña del usuario y por ultimo, crea
       el user. La funcion 'create_superuser' se encarga de lo mismo, con la diferencia de que permite manejar
       los metodos 'is_admin', 'is_staff', e 'is_superuser'. (MyUserManager utiliza el usuario por defecto/incorporado de django) 

    """

    def create_user(self, email, username, password = None):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
        email = self.normalize_email(email),
        username = username,
        password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin, Subscriber):


    """
        Se definen los campos de la clase user personalizada, se crea una instancia de la clase 'HistoricalRecords()' (que no sé para 
        qué sirve),
        se especifica el campo que se permite utilizar como username y el campo requerido. Creamos una instancia de 'MyUserManager()'
        para poder acceder a sus metodos y por ultimo, se definen las funciones '__str__ para mostrar los objetos en el admin de django. 
    
    """

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    notifications = models.ManyToManyField(Notification, default=list)

    historical = HistoricalRecords()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def update(self, task_id, task_status):
        data = {
            "date": datetime.now(),
            "message": f"Task {task_id}: {task_status}",
            "associated_task": task_id
        }
        notifications_obj = Notification.objects.create(**data)
        self.notifications.add(notifications_obj)
