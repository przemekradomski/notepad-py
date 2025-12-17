from django.contrib import admin
from .models import TitleNote, ContentNote, DataNote

# Register your models here.

@admin.register(TitleNote)
class TitleNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'


@admin.register(ContentNote)
class ContentNoteAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['content']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(DataNote)
class DataNoteAdmin(admin.ModelAdmin):
    list_display = ['data_preview', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def data_preview(self, obj):
        return str(obj.data)[:50] + '...' if len(str(obj.data)) > 50 else str(obj.data)
    data_preview.short_description = 'Data'