from django.urls import reverse
from tasks.models import Task
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class ApiTests(APITestCase):
    def test_create_task(self):
        url = reverse('add_task')
        data = {'title': 'Test1', 'description': 'desc', 'completed': False}
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Test1")

    def test_double_create_task(self):
        url = reverse('add_task')
        data = {'title': 'Test1', 'description': 'desc', 'completed': False}
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Test1")
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_empty_desc(self):
        url = reverse('add_task')
        data = {'title': 'Test1', 'description': '', 'completed': False}
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Test1")

    def test_create_task_with_empty_title(self):
        url = reverse('add_task')
        data = {'title': '', 'description': 'testing', 'completed': False}
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_with_wrong_completed(self):
        url = reverse('add_task')
        data = {'title': '', 'description': '', 'completed': '123test'}
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_with_long_fields(self):
        url = reverse('add_task')
        data = {'title': 2600*'f', 'description': 2550*'a', 'completed': False}
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    def test_get_tasks(self):
        url = reverse('get_tasks')
        data = {'title': 'Test1', 'description': 'desc', 'completed': False}
        self.client.post(reverse('add_task'), data, format='json')
        responce = self.client.get(url)
        self.assertGreater(len(responce.data), 0)
        self.assertEqual(responce.data[0]['title'], 'Test1')
        self.assertEqual(responce.data[0]['description'], 'desc')

    def test_update_task(self):
        url = reverse('update_task', kwargs={'pk': 1})
        data1 = {'title': 'Test1', 'description': 'desc', 'completed': False}
        data2 = {'title': 'Test1_updated', 'description': 'desc (updated)', 'completed': True}
        self.client.post(reverse('add_task'), data1, format='json')
        responce = self.client.put(url, data2, format='json')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.data['title'], 'Test1_updated')
        self.assertEqual(responce.data['description'], 'desc (updated)')
        self.assertEqual(responce.data['completed'], True)

    def test_update_task_with_empty_fields(self):
        url = reverse('update_task', kwargs={'pk': 1})
        data1 = {'title': 'Test1', 'description': 'desc', 'completed': False}
        data2 = {'title': '', 'description': '', 'completed': True}
        self.client.post(reverse('add_task'), data1, format='json')
        responce = self.client.put(url, data2, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_with_wrong_completed(self):
        url = reverse('update_task', kwargs={'pk': 1})
        data1 = {'title': 'Test1', 'description': 'desc', 'completed': False}
        data2 = {'title': 'Test1_updated', 'description': 'desc (updated)', 'completed': 'trueee'}
        self.client.post(reverse('add_task'), data1, format='json')
        responce = self.client.put(url, data2, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_empty_task(self):
        url = reverse('update_task', kwargs={'pk': 1})
        data = {'title': 'Test1_updated', 'description': 'desc (updated)', 'completed': True}
        responce = self.client.put(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task(self):
        url = reverse('delete_task', kwargs={'pk': 1})
        data = {'title': 'Test1', 'description': 'desc', 'completed': False}
        self.client.post(reverse('add_task'), data, format='json')
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
        responce = self.client.get(reverse('get_tasks'))
        self.assertEqual(responce.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_empty_task(self):
        url = reverse('delete_task', kwargs={'pk': 1})
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_404_NOT_FOUND)

    def test_double_delete(self):
        url = reverse('delete_task', kwargs={'pk': 1})
        data = {'title': 'Test1', 'description': 'desc', 'completed': False}
        self.client.post(reverse('add_task'), data, format='json')
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
        responce = self.client.delete(url)
        self.assertEqual(responce.status_code, status.HTTP_404_NOT_FOUND)