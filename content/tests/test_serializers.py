from django.test import TestCase
from content.models import Content
from content.serializers import ContentSerializer

class ContentSerializerTest(TestCase):
    def setUp(self):
        self.content = Content.objects.create(
            text="Test content",
            flagged=True,
            categories={'hate': True},
            reviewed=False
        )
        self.serializer = ContentSerializer(instance=self.content)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = {'id', 'text', 'flagged', 'categories', 'reviewed', 'created_at'}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_read_only_fields(self):
        """Test that certain fields are read-only"""
        data = {
            'text': 'New content',
            'flagged': False,  # Should be ignored
            'categories': {'hate': False},  # Should be ignored
            'reviewed': True  # Should be ignored
        }
        serializer = ContentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        content = serializer.save()
        self.assertEqual(content.text, 'New content')
        self.assertFalse(content.flagged)  # Should remain unchanged
        self.assertEqual(content.categories, {})  # Should remain unchanged
        self.assertFalse(content.reviewed)  # Should remain unchanged

    def test_validation(self):
        """Test serializer validation"""
        # Test empty text
        data = {'text': ''}
        serializer = ContentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)

        # Test valid data
        data = {'text': 'Valid content'}
        serializer = ContentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
