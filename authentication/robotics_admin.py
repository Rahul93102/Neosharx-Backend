from django.contrib import admin
from . import models

@admin.register(models.RoboticsNews)
class RoboticsNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'is_featured', 'is_breaking', 'is_published', 'views_count', 'created_at')
    list_filter = ('is_featured', 'is_breaking', 'is_published', 'category', 'priority', 'difficulty_level', 'created_at')
    search_fields = ('title', 'subtitle', 'summary', 'content', 'author_name', 'company_mentioned', 'technology_focus')
    readonly_fields = ('slug', 'views_count', 'likes_count', 'shares_count', 'comments_count', 'created_at', 'updated_at', 'published_at', 'youtube_embed_url')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'subtitle', 'slug', 'priority', 'difficulty_level')
        }),
        ('Content', {
            'fields': ('summary', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'additional_images', 'video_url', 'youtube_embed_url')
        }),
        ('Featured Screen', {
            'fields': ('featured_screen',),
            'description': 'Add a single featured screen (image or video) as JSON object. Example: {"url": "https://example.com/image.jpg", "type": "image", "is_featured": true} or {"url": "https://youtube.com/watch?v=xyz", "type": "video", "is_featured": true}'
        }),
        ('Categorization', {
            'fields': ('category', 'tags', 'robot_type', 'technology_focus')
        }),
        ('Source & Attribution', {
            'fields': ('author_name', 'source_name', 'source_url', 'company_mentioned')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'is_breaking', 'published_at', 'reading_time')
        }),
        ('Engagement Metrics', {
            'fields': ('views_count', 'likes_count', 'shares_count', 'comments_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_published', 'mark_as_breaking', 'reset_engagement']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} articles marked as featured.')
    mark_as_featured.short_description = "Mark selected articles as featured"
    
    def mark_as_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f'{queryset.count()} articles published.')
    mark_as_published.short_description = "Publish selected articles"
    
    def mark_as_breaking(self, request, queryset):
        queryset.update(is_breaking=True)
        self.message_user(request, f'{queryset.count()} articles marked as breaking news.')
    mark_as_breaking.short_description = "Mark as breaking news"
    
    def reset_engagement(self, request, queryset):
        queryset.update(views_count=0, likes_count=0, shares_count=0, comments_count=0)
        self.message_user(request, f'Engagement metrics reset for {queryset.count()} articles.')
    reset_engagement.short_description = "Reset engagement metrics to 0"