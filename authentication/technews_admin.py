"""
Django Admin configuration for TechNews model
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import TechNews

@admin.register(TechNews)
class TechNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'author_name', 'views_count', 'is_featured', 'is_breaking', 'is_published', 'published_at')
    list_filter = ('category', 'priority', 'is_published', 'is_featured', 'is_breaking', 'is_trending', 'published_at')
    search_fields = ('title', 'subtitle', 'excerpt', 'content', 'author_name', 'tags')
    readonly_fields = ('slug', 'views_count', 'likes_count', 'shares_count', 'created_at', 'updated_at', 'engagement_score_display')
    prepopulated_fields = {}  # slug auto-generated in model
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'subtitle', 'excerpt', 'content', 'category'),
            'description': 'Essential article information'
        }),
        ('Media', {
            'fields': ('featured_image', 'thumbnail_image', 'video_url', 'gallery_images'),
            'description': 'Images and video content'
        }),
        ('Featured Screen', {
            'fields': ('featured_screen',),
            'description': '''
            Featured Screen Configuration (JSON format):
            {"url": "https://image-or-video-url.com", "type": "image", "is_featured": true}
            - url: Direct link to image or video
            - type: "image" or "video" 
            - is_featured: true to show in featured slider, false to hide
            '''
        }),
        ('Author & Source', {
            'fields': ('author_name', 'author_bio', 'author_avatar', 'source_name', 'source_url'),
            'description': 'Attribution and source information'
        }),
        ('Classification', {
            'fields': ('tags', 'priority', 'read_time_minutes'),
            'description': '''
            Tags JSON format: ["AI", "Machine Learning", "OpenAI"]
            '''
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'is_breaking', 'is_trending', 'published_at'),
            'description': 'Control article visibility and promotion'
        }),
        ('Engagement', {
            'fields': ('views_count', 'likes_count', 'shares_count', 'engagement_score_display'),
            'description': 'Article engagement metrics (read-only)'
        }),
        ('Related Content', {
            'fields': ('related_links', 'key_points'),
            'description': '''
            Related Links JSON: [{"title": "Link Title", "url": "https://..."}]
            Key Points JSON: ["Key point 1", "Key point 2", "Key point 3"]
            '''
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'description': 'Search engine optimization'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def engagement_score_display(self, obj):
        """Display engagement score in admin"""
        score = obj.engagement_score
        if score > 1000:
            color = 'green'
        elif score > 500:
            color = 'orange'
        else:
            color = 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, score
        )
    engagement_score_display.short_description = 'Engagement Score'
    
    actions = ['publish_articles', 'unpublish_articles', 'feature_articles', 'unfeature_articles', 'mark_as_breaking']
    
    def publish_articles(self, request, queryset):
        """Bulk publish articles"""
        from django.utils import timezone
        for article in queryset:
            if not article.published_at:
                article.published_at = timezone.now()
            article.is_published = True
            article.save()
        self.message_user(request, f"{queryset.count()} article(s) published successfully.")
    publish_articles.short_description = "Publish selected articles"
    
    def unpublish_articles(self, request, queryset):
        """Bulk unpublish articles"""
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} article(s) unpublished.")
    unpublish_articles.short_description = "Unpublish selected articles"
    
    def feature_articles(self, request, queryset):
        """Bulk feature articles"""
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} article(s) featured.")
    feature_articles.short_description = "Feature selected articles"
    
    def unfeature_articles(self, request, queryset):
        """Bulk unfeature articles"""
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} article(s) unfeatured.")
    unfeature_articles.short_description = "Unfeature selected articles"
    
    def mark_as_breaking(self, request, queryset):
        """Mark articles as breaking news"""
        queryset.update(is_breaking=True, priority='breaking')
        self.message_user(request, f"{queryset.count()} article(s) marked as breaking news.")
    mark_as_breaking.short_description = "Mark as breaking news"
