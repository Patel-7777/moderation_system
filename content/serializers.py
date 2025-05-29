from rest_framework import serializers
from .models import Content

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "text", "flagged", "categories", "reviewed", "created_at"]
        read_only_fields = ["id", "flagged", "categories", "reviewed", "created_at"] 