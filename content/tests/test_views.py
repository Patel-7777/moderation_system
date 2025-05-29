from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from content.models import Content

class ContentSubmissionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('content-submit')

    @patch('content.views.moderate_content.delay')
    def test_successful_content_submission(self, mock_task):
        """Test successful content submission"""
        data = {'text': 'Test content for API'}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Content.objects.count(), 1)
        content = Content.objects.get()
        self.assertEqual(content.text, 'Test content for API')
        mock_task.assert_called_once_with(content.id)

    def test_invalid_content_submission(self):
        """Test content submission with invalid data"""
        # Test empty text
        data = {'text': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Content.objects.count(), 0)

        # Test missing text field
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Content.objects.count(), 0)

    def test_content_submission_response_format(self):
        """Test the response format of content submission"""
        data = {'text': 'Test content'}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data
        self.assertIn('id', response_data)
        self.assertIn('text', response_data)
        self.assertIn('flagged', response_data)
        self.assertIn('categories', response_data)
        self.assertIn('reviewed', response_data)
        self.assertIn('created_at', response_data)
