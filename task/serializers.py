from rest_framework import serializers
from task.models import SubTaskItem, SubTask, Task

class SubTaksItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTaskItem
        fields = '__all__'

class SubTaskSerializer(serializers.ModelSerializer):

    item = SubTaksItemSerializer(many=True)

    class Meta:
        model = SubTask
        fields = '__all__'

    def get_item(self, instance):
        return list(instance.item.values())
    
    def get_item_two(self, instance):
        return list(instance.item.values())

class TaskSerializer(serializers.ModelSerializer):

    sub_tasks = SubTaskSerializer(many=True) # de la relacion many to many

    class Meta:
        model = Task
        fields = '__all__'
    
    def get_sub_tasks(self, instance): # this
        return list(instance.sub_tasks.values())
    
    def create(self, validated_data):
        sub_task_data = validated_data.pop('sub_tasks', [])
        task = Task.objects.create(**validated_data)
        sub_task_array = []
        
        for sub_task in sub_task_data:
            task_item_data = sub_task.pop('item', [])
            sub_task_obj = SubTask.objects.create(**sub_task)
            sub_task_array.append(sub_task_obj)
            task_item_array = []
            for sub_task_item in task_item_data:
                sub_task_item_obj = SubTaskItem.objects.create(**sub_task_item)
                task_item_array.append(sub_task_item_obj)
            sub_task_obj.item.set(task_item_array)
        task.sub_tasks.set(sub_task_array)
        task.save()
        return task
    
    def update(self, pk, validated_data):
        """
            Bloque Task
        """
        sub_task_data = validated_data.pop('sub_tasks', [])

        task = Task.objects.get(task_id=pk.task_id) # Filtramos y actualizamos
       
        if task.task_status != validated_data["task_status"]:
            task.notify(validated_data["task_status"])
        
        task.subscribers = validated_data["subscribers"]
        task.task_name = validated_data["task_name"]
        task.task_date = validated_data["task_date"]
        task.task_description = validated_data["task_description"]
        task.task_category = validated_data["task_category"]
        task.task_users_id = validated_data["task_users_id"]
        task.task_priority = validated_data["task_priority"]
        task.task_status = validated_data["task_status"]
        task.task_id = validated_data["task_id"]
        
        sub_task_array = []
        for sub_task in sub_task_data:
            """
                Bloque SubTask
            """
            # se guardan los items del campo "item" dentro de una variable
            items = sub_task.pop('item', [])
            # creamos un indice que nos servira para filtrar la sub_task por id.
            index = len(sub_task_array)
            # utilizamos la funcion de listar del serializer para obtener las sub_tasks.
            asd = self.get_sub_tasks(task)
            # hacemos una query para obtener el objeto de tipo SubTask correspondiente (utilizando el id como filtro en nuestra lista de sub_tasks).
            sub_task_obj = SubTask.objects.get(pk=asd[index]['id'])
            # editamos los campos que queramos.
            sub_task_obj.name = sub_task["name"]
            # agregamos el objeto ya editado al array "sub_task_array" el cual al final se aplicara al objeto Task
            sub_task_array.append(sub_task_obj)

            # comenzamos otro bucle for, en el cual tendremos que hacer lo mismo que se hizo para el bloque de SubTask
            task_item_array = []
            for sub_task_item in items:
                """
                    Bloque SubTaskItem
                """
            
                index = len(task_item_array)
                new = SubTaskSerializer
                
                sub_task_items = new.get_item_two(self,sub_task_obj)
                sub_task_item_obj = SubTaskItem.objects.get(pk=sub_task_items[index]["id"])
                
                sub_task_item_obj.done = sub_task_item["done"]
                sub_task_item_obj.item = sub_task_item["item"]
                
                task_item_array.append(sub_task_item_obj)
            sub_task_obj.item.set(task_item_array)
        task.sub_tasks.set(sub_task_array)
        task.save()
        
        return task