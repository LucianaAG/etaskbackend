from django.db import models
from abc import ABC, abstractmethod



class Publisher:
    """
        Tiene la funcion de aceptar nuevos observadores, eliminarlos y tambien de notificar cuando hay un cambio en un campo concreto.
    """
    @abstractmethod
    def attach(self):
        pass
    
    @abstractmethod
    def dettach(self):
        pass
    
    @abstractmethod
    def notify(self):
        pass

class Subscriber:

    @abstractmethod
    def update(self):
        # El resultado esperado es que el subscriptor obtenga un mensaje a modo de print del nuevo estado de la tarea.

        # Mensaje esperado:
        # "Task 1: Completado."
        # "Task {id}: {task_status}"
        pass

class Notification(models.Model):
      
      date = models.DateField()
      message = models.CharField(max_length=100)
      associated_task = models.IntegerField(null=True, blank=True)