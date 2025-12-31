from rest_framework.test import APITestCase
from .models import Task
import os


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.api_key = os.environ.get('API_KEY', 'test-api-key')
        os.environ['API_KEY'] = self.api_key
        self.client.credentials(HTTP_X_API_KEY=self.api_key)

    def test_create_task_without_title_returns_400(self):
        url = '/api/tasks/'
        payload = {
            'description': 'no title here',
            'status': 'BACKLOG',
            'priority': 'LOW'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.json())

    def test_update_task_status_succeeds_and_persists(self):
        task = Task.objects.create(title='Test task', status='BACKLOG', priority='MEDIUM')
        url = f'/api/tasks/{task.pk}/'
        payload = {'status': 'IN_PROGRESS', 'title': task.title, 'priority': task.priority}
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, 'IN_PROGRESS')

    def test_delete_task_removes_from_db(self):
        task = Task.objects.create(title='To be deleted', status='BACKLOG', priority='LOW')
        url = f'/api/tasks/{task.pk}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        exists = Task.objects.filter(pk=task.pk).exists()
        self.assertFalse(exists)
