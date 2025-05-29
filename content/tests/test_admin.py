from django.test import TestCase
from content.models import Content
from content.admin import ContentAdmin

class ContentAdminTest(TestCase):
    def setUp(self):
        self.content1 = Content.objects.create(
            text="Test content 1",
            flagged=True,
            categories={'hate': True},
            reviewed=False
        )
        self.content2 = Content.objects.create(
            text="Test content 2",
            flagged=False,
            categories={},
            reviewed=False
        )
        self.admin = ContentAdmin(Content, None)

    def test_mark_as_reviewed_action(self):
        """Test marking multiple contents as reviewed"""
        queryset = Content.objects.filter(id__in=[self.content1.id, self.content2.id])
        
        self.admin.mark_as_reviewed(None, queryset)
        
        self.content1.refresh_from_db()
        self.content2.refresh_from_db()
        self.assertTrue(self.content1.reviewed)
        self.assertTrue(self.content2.reviewed)

    def test_override_flagged_action(self):
        """Test overriding flagged status and marking as reviewed"""
        queryset = Content.objects.filter(id=self.content1.id)
        
        self.admin.override_flagged(None, queryset)
        
        self.content1.refresh_from_db()
        self.assertFalse(self.content1.flagged)
        self.assertTrue(self.content1.reviewed)

    def test_list_display(self):
        """Test that list_display contains all required fields"""
        expected_fields = ['id', 'text', 'flagged', 'categories', 'reviewed', 'created_at']
        self.assertEqual(self.admin.list_display, expected_fields)

    def test_list_filter(self):
        """Test that list_filter contains all required fields"""
        expected_filters = ['flagged', 'reviewed', 'created_at']
        self.assertEqual(self.admin.list_filter, expected_filters)

    def test_search_fields(self):
        """Test that search_fields contains the text field"""
        self.assertEqual(self.admin.search_fields, ['text'])
