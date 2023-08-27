from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from task.models import Task
from task.serializers import TaskSerializer
from user.authentication_mixins import Authentication

# Create your views here.

class TaskItemViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    model_to_format = "Task"
    queryset = Task.objects.all()

    def retrieve(self, request, pk): # get
        task_item = Task.objects.get(task_id=pk)
        serializer = self.get_serializer(task_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):# post
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk): # put

        task_item = Task.objects.get(task_id=pk)
        
        serializer = self.serializer_class(task_item, data=request.data)# serializamos

        if serializer.is_valid(): # validamos
            self.perform_update(serializer) # guardamos
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk): # delete
        if self.get_queryset().filter(task_id=pk).first() != None:
            task_item = self.get_queryset().filter(task_id=pk).first()
            task_item.delete()
            task_item.save()
            return Response({'message':'[*] {} deleted successfully.'.format(self.model_to_format)}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error':"[!] Can't access to that resource."}, status=status.HTTP_400_BAD_REQUEST)
