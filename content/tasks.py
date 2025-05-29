from celery import shared_task
from django.conf import settings
from .models import Content
import openai

def get_openai_client():
    return openai.OpenAI(api_key=settings.OPENAI_API_KEY)

@shared_task
def moderate_content(content_id):
    content = Content.objects.get(id=content_id)
    client = get_openai_client()
    response = client.moderations.create(input=content.text)
    result = response.results[0]
    content.flagged = result.flagged
    content.categories = result.categories
    content.save()
    return content.flagged 