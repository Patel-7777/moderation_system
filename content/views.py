from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Content
from .serializers import ContentSerializer
from .tasks import moderate_content

# Create your views here.

class ContentSubmissionView(APIView):
    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            moderate_content.delay(content.id)
            return Response(ContentSerializer(content).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
