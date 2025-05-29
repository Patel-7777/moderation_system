from django.test import TestCase
from unittest.mock import patch, MagicMock
from content.models import Content
from content.tasks import moderate_content

class ContentModerationTaskTest(TestCase):
    def setUp(self):
        self.content = Content.objects.create(
            text="Test content for moderation",
            flagged=False,
            categories={},
            reviewed=False
        )

    @patch('content.tasks.get_openai_client')
    def test_moderation_task_success(self, mock_client):
        """Test successful moderation task execution"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.results = [MagicMock(
            flagged=True,
            categories={
                'hate': True,
                'hate/threatening': False,
                'self-harm': False,
                'sexual': False,
                'sexual/minors': False,
                'violence': False,
                'violence/graphic': False
            }
        )]
        mock_client.return_value.moderations.create.return_value = mock_response

        # Run the task
        result = moderate_content(self.content.id)

        # Refresh content from database
        self.content.refresh_from_db()

        # Assertions
        self.assertTrue(result)
        self.assertTrue(self.content.flagged)
        self.assertEqual(
            self.content.categories,
            {
                'hate': True,
                'hate/threatening': False,
                'self-harm': False,
                'sexual': False,
                'sexual/minors': False,
                'violence': False,
                'violence/graphic': False
            }
        )

    @patch('content.tasks.get_openai_client')
    def test_moderation_task_no_flag(self, mock_client):
        """Test moderation task when content is not flagged"""
        # Mock OpenAI response for non-flagged content
        mock_response = MagicMock()
        mock_response.results = [MagicMock(
            flagged=False,
            categories={
                'hate': False,
                'hate/threatening': False,
                'self-harm': False,
                'sexual': False,
                'sexual/minors': False,
                'violence': False,
                'violence/graphic': False
            }
        )]
        mock_client.return_value.moderations.create.return_value = mock_response

        # Run the task
        result = moderate_content(self.content.id)

        # Refresh content from database
        self.content.refresh_from_db()

        # Assertions
        self.assertFalse(result)
        self.assertFalse(self.content.flagged)
        self.assertEqual(
            self.content.categories,
            {
                'hate': False,
                'hate/threatening': False,
                'self-harm': False,
                'sexual': False,
                'sexual/minors': False,
                'violence': False,
                'violence/graphic': False
            }
        )

    @patch('content.tasks.get_openai_client')
    def test_moderation_task_error_handling(self, mock_client):
        """Test moderation task error handling"""
        # Mock OpenAI client to raise an exception
        mock_client.return_value.moderations.create.side_effect = Exception("API Error")

        # Run the task and expect it to raise the exception
        with self.assertRaises(Exception):
            moderate_content(self.content.id)

        # Content should remain unchanged
        self.content.refresh_from_db()
        self.assertFalse(self.content.flagged)
        self.assertEqual(self.content.categories, {})
