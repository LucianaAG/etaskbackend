from rest_framework import status
from task.models import SubTask, SubTaskItem, Task
from task.test_setup import TestSetUp

# Create your tests here.


class TestViewSets(TestSetUp):

    def test_list(self): # test metodo GET
        response = self.client.get(
            '/tasks/',
            headers=self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        task = Task.objects.create(
            task_name="developer",
            task_date="2023-08-15",
            task_description="x",
            task_category="category",
            task_users_id=[],
            task_priority="3",
            task_status="status",
            task_id="1"
        )
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
        task.sub_tasks.set([sub_task_obj])
        task.save()
        response = self.client.get(
            '/tasks/1/',
            headers=self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self): # test metodo POST
        response = self.client.post(
           '/tasks/',
            {
                "task_name": "developer",
                "task_date": "2023-08-15",
                "task_description": "x",
                "task_category": "category",
                "task_users_id": [],
                "task_priority": "3",
                "task_status": "status",
                "task_id": "4",
                "sub_tasks": []
            },
            format='json',
            headers = self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):

        task = Task.objects.create(
            task_name="ddd",
            task_date="2023-08-15",
            task_description="x",
            task_category="category",
            task_users_id=[],
            task_priority="3",
            task_status="status",
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

        response = self.client.put(
            '/tasks/1/',   
            {
                "subscribers": [],
                "task_name": "lll",
                "task_date": "2023-08-15",
                "task_description": "x",
                "task_category": "category",
                "task_users_id": [],
                "task_priority": "3",
                "task_status": "failed",
                "task_id": "1",
                "sub_tasks": []
            },
            format='json'
        ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #self.assertEqual(response.content, status.HTTP_200_OK)
        


    def test_delete(self): # test metodo DELETE
        task = Task.objects.create(
            task_name="developer",
            task_date="2023-08-15",
            task_description="x",
            task_category="category",
            task_users_id=[],
            task_priority="3",
            task_status="status",
            task_id="1"
        )
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
        task.sub_tasks.set([sub_task_obj])
        task.save()

        response=self.client.delete(
            '/tasks/1/',
            headers =  self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# tests en caso de error
    
    def test_create_invalid(self): # test metodo POST invalido
        response=self.client.post(
           '/tasks/',
            {
                "task_name": "developer",
                "task_date": "2023-08-15",
                "task_description": "x",
                "task_category": "category",
                "task_users_id": [],
                "task_priority": "3",
                "task_status": "status",
                "task_id": "4",
                "sub_tasks": []
            },
            headers = self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_invalid(self): # test metodo DELETE invalido
        task = Task.objects.create(
            task_name="developer",
            task_date="2023-08-15",
            task_description="x",
            task_category="category",
            task_users_id=[],
            task_priority="3",
            task_status="status",
            task_id="1"
        )
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
        task.sub_tasks.set([sub_task_obj])
        task.save()

        response=self.client.delete(
            '/tasks/2/',
            headers =  self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
# tests en caso de falta de autorización 

    def test_list_not_auth(self):
        self.logout()
        response = self.client.get(
            '/tasks/',
            headers=self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_not_auth(self):
        self.logout()
        response = self.client.post(
            '/tasks/',
            {
                "task_name": "developer",
                "task_date": "2023-08-15",
                "task_description": "x",
                "task_category": "category",
                "task_users_id": [],
                "task_priority": "3",
                "task_status": "status",
                "task_id": "4",
                "sub_tasks": []
            },
            format='json',
            headers = self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_not_auth(self):
        self.logout()
        response = self.client.delete(
            '/tasks/1/',
            headers = self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)