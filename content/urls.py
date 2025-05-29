from django.urls import path
from .views import ContentSubmissionView

urlpatterns = [
    path('content/', ContentSubmissionView.as_view(), name='content-submit'),
] 