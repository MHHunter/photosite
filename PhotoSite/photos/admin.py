from django.contrib import admin
from .models import Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'visibility', 'likes', 'uploaded_at')
    search_fields = ('user__username', 'caption')
    list_filter = ('visibility', 'uploaded_at')
