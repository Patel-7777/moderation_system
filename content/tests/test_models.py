from django.test import TestCase
from content.models import Content

class ContentModelTest(TestCase):
    def setUp(self):
        self.content = Content.objects.create(
            text="Test content",
            flagged=False,
            categories={},
            reviewed=False
        )

    def test_content_creation(self):
        """Test that content is created with correct default values"""
        self.assertEqual(self.content.text, "Test content")
        self.assertFalse(self.content.flagged)
        self.assertFalse(self.content.reviewed)
        self.assertEqual(self.content.categories, {})

    def test_content_str_representation(self):
        """Test the string representation of the Content model"""
        self.assertEqual(str(self.content), f"Content {self.content.id}")

    def test_content_with_categories(self):
        """Test content creation with predefined categories"""
        categories = {
            'hate': True,
            'violence': False
        }
        content = Content.objects.create(
            text="Content with categories",
            flagged=True,
            categories=categories,
            reviewed=False
        )
        self.assertEqual(content.categories, categories)
        self.assertTrue(content.flagged)
