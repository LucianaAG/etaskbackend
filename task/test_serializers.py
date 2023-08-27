from datetime import datetime
from django.test import TestCase
from task.models import SubTask, SubTaskItem, Task
from task.serializers import SubTaskSerializer, TaskSerializer


class TestSubTaskSerializer(TestCase):

    def test_get_item(self):
        # 1- Configuracion (setup) de todo lo que se necesita para que el metodo funcione. (Opcional)

        # 2- Creacion de objetos ficticios para pasarle al metodo (Opcional).
        sub_task_obj = SubTask.objects.create(
            name="task_example",
            id="1"
        )
        sub_task_item_obj = SubTaskItem.objects.create(
            item="item_1",
            done=False,
            id="1"
        )

        sub_task_obj.item.set([sub_task_item_obj])

        serializer = SubTaskSerializer(instance=sub_task_obj)
        expected_items = list(sub_task_obj.item.values())

        # 3- Ejecutar el metodo que vamos a testear y obtener la respuesta.
        actual_items = serializer.get_item(sub_task_obj)

        # 3- Ejecutar el metodo que vamos a testear y obtener la respuesta.
        self.assertEqual(actual_items, expected_items)
    
    def test_get_item_two(self):

        sub_task_obj = SubTask.objects.create(
            name="task_example",
            id="1"
        )
        sub_task_item_obj = SubTaskItem.objects.create(
            item="item_1",
            done=False,
            id="1"
        )

        sub_task_obj.item.set([sub_task_item_obj])

        serializer = SubTaskSerializer(instance=sub_task_obj)
        expected_items = list(sub_task_obj.item.values())

        actual_items = serializer.get_item_two(sub_task_obj)

        self.assertEqual(actual_items, expected_items)



class TestTaskSerializer(TestCase):

    def test_get_sub_tasks(self):

        task_object = Task.objects.create(
            task_name="developer",
            task_date="2023-08-15",
            task_description="x",
            task_category="category",
            task_users_id=[],
            task_priority="3",
            task_status="status",
            task_id="1"
        )

        sub_task_object = SubTask.objects.create(  
            name="dev",
            id="1",
        )
        item = SubTaskItem.objects.create(
            item='asd',
            done=True,
            id='1'
        )
        sub_task_object.item.add(item)
        task_object.sub_tasks.set([sub_task_object])
        task_object.save()

        serializer = TaskSerializer(instance=task_object)

        expected_items = list(task_object.sub_tasks.values())

        actual_items = serializer.get_sub_tasks(task_object)

        self.assertEqual(actual_items, expected_items)

    def test_create(self):
        # 1- Configuracion (setup) de todo lo que se necesita para que el metodo funcione. (Opcional)

        # 2- Creacion de objetos ficticios para pasarle al metodo (Opcional).

        validated_data = {
            'task_id': '4',  
            'subscribers': [],
            'task_name': 'developer', 
            'task_date': '2023-8-15', 
            'task_description': 'x', 
            'task_category': 'category', 
            'task_users_id': [], 
            'task_priority': '3', 
            'task_status': 'Failed',
            'sub_tasks': [
                {
                    'name': 'dev', 
                    'id': '1', 
                    'item': [
                        {
                            'item': 'asd', 
                            'done': True, 
                            'id': '1'
                        }
                    ]
                }
            ]
        }

        # 3- Ejecutar el metodo que vamos a testear y obtener la respuesta.
        serializer = TaskSerializer()
        response = serializer.create(validated_data)
        # 4- Evaluar la respuesta.
        self.assertTrue(isinstance(response, Task))

    
    def test_update(self):

        task = Task.objects.create(
            task_name="ddd",
            task_date="2023-08-15",
            task_description="x",
            task_category="category",
            task_users_id=[],
            task_priority="3",
            task_status="Failed",
            task_id="1"
        )
        sub_task_obj = SubTask.objects.create(
            name="dev",
            id="1"
        )
        sub_task_item_obj = SubTaskItem.objects.create(
            item="asd",
            done=False,
            id="1"
        )

        sub_task_obj.item.set([sub_task_item_obj])
        task.sub_tasks.set([sub_task_obj])
        task.save()
    
        validated_data = {
            'task_id': '1',  
            'subscribers': [],
            'task_name': 'developer', 
            'task_date': '2023-8-15', 
            'task_description': 'x', 
            'task_category': 'category', 
            'task_users_id': [], 
            'task_priority': '3', 
            'task_status': 'Failed',
            'sub_tasks': [
                {
                    'name': 'secundaria', 
                    'id': '1', 
                    'item': [
                        {
                            'item': 'asd', 
                            'done': True, 
                            'id': '1'
                        }
                    ]
                }
            ]
        }
        serializer = TaskSerializer()

        response = serializer.update(task, validated_data)

        self.assertTrue(isinstance(response, Task))
    
    