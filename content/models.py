from django.db import models

# Create your models here.

class Content(models.Model):
    text = models.TextField()
    flagged = models.BooleanField(default=False)
    categories = models.JSONField(default=dict, blank=True)
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Content {self.id}"
