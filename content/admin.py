from django.contrib import admin
from .models import Content

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "flagged", "categories", "reviewed", "created_at")
    list_filter = ("flagged", "reviewed", "created_at")
    search_fields = ("text",)
    actions = ["mark_as_reviewed", "override_flagged"]

    def mark_as_reviewed(self, request, queryset):
        queryset.update(reviewed=True)
    mark_as_reviewed.short_description = "Mark selected as reviewed"

    def override_flagged(self, request, queryset):
        queryset.update(flagged=False, reviewed=True)
    override_flagged.short_description = "Override flagged and mark as reviewed"
